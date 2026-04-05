"""Lightweight custom HTML dashboard reporter for pytest.

This plugin captures per-test results and emits a rich, self-contained HTML
dashboard with charts, summary cards, and detailed analytics. It is designed to
complement the existing `pytest-html` output with a more visual, executive view
of the run.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import platform
import socket
import statistics
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

import pytest


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("dashboard", "Custom rich HTML dashboard report")
    group.addoption(
        "--dashboard-report",
        action="store",
        default="reports/dashboard.html",
        help="Path to write the interactive dashboard HTML report.",
    )


def pytest_configure(config: pytest.Config) -> None:
    if getattr(config, "workerinput", None) is not None:
        return

    if getattr(config, "_dashboard_reporter", None):
        return

    output = Path(config.getoption("--dashboard-report"))
    plugin = _DashboardReporter(output, config)
    config._dashboard_reporter = plugin
    config.pluginmanager.register(plugin, "dashboard-reporter")


def pytest_unconfigure(config: pytest.Config) -> None:
    plugin = getattr(config, "_dashboard_reporter", None)
    if plugin:
        config.pluginmanager.unregister(plugin)
        config._dashboard_reporter = None


class _DashboardReporter:
    def __init__(self, output_path: Path, config: pytest.Config) -> None:
        self.output_path = output_path
        self.config = config
        self.start_time = _dt.datetime.utcnow()
        self.results: Dict[str, Dict[str, Any]] = {}
        self.collected = 0

    # --- collection hooks -------------------------------------------------
    def pytest_collection_finish(self, session: pytest.Session) -> None:
        self.collected = len(getattr(session, "items", []))

    # --- runtime hooks ----------------------------------------------------
    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        # Only handle actual test outcomes; collect reports also flow through here
        if report.when not in {"setup", "call", "teardown"}:
            return

        entry = self.results.setdefault(report.nodeid, self._base_entry(report))
        entry["duration"] += getattr(report, "duration", 0.0) or 0.0
        entry["keywords"] = self._keyword_list(report)

        if getattr(report, "wasxfail", None):
            if report.skipped:
                entry["outcome"] = "xfailed"
                entry["reason"] = str(report.wasxfail)
            elif report.passed:
                entry["outcome"] = "xpassed"
                entry["reason"] = str(report.wasxfail)
            return

        if report.failed:
            entry["outcome"] = "failed"
            entry["fail_stage"] = report.when
            entry["error"] = self._trim_longrepr(report)
        elif report.skipped:
            entry["outcome"] = "skipped"
            entry["reason"] = self._skip_reason(report)
        elif report.when == "call" and entry["outcome"] is None:
            entry["outcome"] = "passed"

    def pytest_sessionfinish(self, session: pytest.Session, exitstatus: int) -> None:
        if getattr(self.config, "workerinput", None) is not None:
            return

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        payload = self._build_payload(exitstatus)
        self.output_path.write_text(self._render_html(payload), encoding="utf-8")

    def pytest_terminal_summary(self, terminalreporter: pytest.TerminalReporter) -> None:
        if getattr(self.config, "workerinput", None) is not None:
            return
        rel = self.output_path
        terminalreporter.write_sep("=", f"dashboard report written to {rel}")

    # --- helpers ----------------------------------------------------------
    def _base_entry(self, report: pytest.TestReport) -> Dict[str, Any]:
        path, line, _ = report.location
        return {
            "nodeid": report.nodeid,
            "name": report.nodeid.split("::")[-1],
            "file": str(path),
            "line": line + 1,
            "keywords": [],
            "duration": 0.0,
            "outcome": None,
            "fail_stage": None,
            "error": "",
            "reason": "",
        }

    def _keyword_list(self, report: pytest.TestReport) -> List[str]:
        # Filter internal pytest keywords for a cleaner display
        internal = {"pytestmark", "python", "builtins", "request"}
        return sorted(k for k, v in report.keywords.items() if v and k not in internal)

    def _skip_reason(self, report: pytest.TestReport) -> str:
        if isinstance(report.longrepr, tuple) and len(report.longrepr) >= 3:
            return str(report.longrepr[2])
        if hasattr(report, "wasxfail") and report.wasxfail:
            return str(report.wasxfail)
        text = getattr(report, "longreprtext", "")
        return text.split("\n")[0] if text else ""

    def _trim_longrepr(self, report: pytest.TestReport, limit: int = 2200) -> str:
        text = getattr(report, "longreprtext", "") or str(report.longrepr)
        text = text.strip()
        if len(text) > limit:
            return text[: limit - 3] + "..."
        return text

    def _build_payload(self, exitstatus: int) -> Dict[str, Any]:
        tests = list(self.results.values())
        total = len(tests)
        counts = Counter(t["outcome"] or "unknown" for t in tests)
        durations = [t["duration"] for t in tests if t["duration"]]
        wall_clock = (_dt.datetime.utcnow() - self.start_time).total_seconds()

        slow_tests = sorted(tests, key=lambda x: x["duration"], reverse=True)[:8]
        marker_counts = Counter(
            m for t in tests for m in t.get("keywords", []) if m not in {"skip", "xfail"}
        )
        file_counts = Counter(Path(t["file"]).name for t in tests)

        pass_rate = (counts.get("passed", 0) / total * 100) if total else 0.0
        avg_duration = statistics.mean(durations) if durations else 0.0
        median_duration = statistics.median(durations) if durations else 0.0

        insights = self._generate_insights(counts, pass_rate, slow_tests, file_counts)

        return {
            "created_at": _dt.datetime.utcnow().isoformat() + "Z",
            "summary": {
                "collected": self.collected or total,
                "executed": total,
                "wall_clock": wall_clock,
                "avg_duration": avg_duration,
                "median_duration": median_duration,
                "pass_rate": pass_rate,
                "counts": counts,
                "exitstatus": exitstatus,
            },
            "environment": {
                "python": platform.python_version(),
                "pytest": pytest.__version__,
                "hostname": socket.gethostname(),
                "os": platform.platform(),
                "base_url": os.getenv("BASE_URL", "not set"),
                "api_base_url": os.getenv("API_BASE_URL", "not set"),
                "browser": os.getenv("BROWSER", "not set"),
                "workers": self.config.getvalue("numprocesses") or 1,
            },
            "slow_tests": slow_tests,
            "markers": marker_counts,
            "files": file_counts,
            "tests": tests,
            "insights": insights,
        }

    def _generate_insights(
        self,
        counts: Counter,
        pass_rate: float,
        slow_tests: List[Dict[str, Any]],
        file_counts: Counter,
    ) -> List[str]:
        insights: List[str] = []
        total = sum(counts.values()) or 1
        failures = counts.get("failed", 0)
        skips = counts.get("skipped", 0)

        insights.append(f"Pass rate is {pass_rate:.1f}% across {total} executed tests.")

        if failures:
            touched = len([c for c in file_counts if c])
            insights.append(
                f"{failures} failure(s) spread across {touched} file(s); prioritise these first."
            )
        elif pass_rate == 100 and total:
            insights.append("All executed tests passed; consider tightening thresholds or adding negative cases.")

        if skips:
            insights.append(f"{skips} test(s) skipped; review markers to ensure intentional coverage gaps only.")

        if slow_tests:
            top = slow_tests[0]
            total_runtime = sum(t["duration"] for t in slow_tests) or 0.0
            if total_runtime:
                pct = (top["duration"] / total_runtime) * 100
                insights.append(
                    f"Slowest test '{top['name']}' consumes {pct:.1f}% of tracked runtime; optimise or parallelise."
                )

        return insights

    def _render_html(self, payload: Dict[str, Any]) -> str:
        data_json = json.dumps(payload, ensure_ascii=True)
        passed = payload["summary"]["counts"].get("passed", 0)
        failed = payload["summary"]["counts"].get("failed", 0)
        skipped = payload["summary"]["counts"].get("skipped", 0)
        insights_html = "".join(f"<li>{item}</li>" for item in payload["insights"]) or '<li class="muted">No insights generated</li>'
        markers_html = "".join(f'<span class="badge">{k}: {v}</span>' for k, v in payload["markers"].items()) or '<span class="muted">No markers detected</span>'
        files_html = "".join(f'<span class="badge">{k}: {v}</span>' for k, v in payload["files"].items()) or '<span class="muted">No files reported</span>'
        rows_html = "".join(self._render_row(t) for t in payload["tests"])

        template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Test Run Dashboard</title>
  <style>
    :root {
      --bg: #0b1020;
      --panel: #0f172a;
      --border: #1f2937;
      --muted: #94a3b8;
      --text: #e5e7eb;
      --pass: #10b981;
      --fail: #f43f5e;
      --skip: #fbbf24;
      --info: #38bdf8;
      --accent: linear-gradient(135deg, #0ea5e9, #22c55e);
      --shadow: 0 18px 50px rgba(8, 47, 73, 0.35);
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      padding: 32px;
      background: radial-gradient(circle at 20% 20%, rgba(34,197,94,0.12), transparent 25%),
                  radial-gradient(circle at 80% 0%, rgba(56,189,248,0.16), transparent 25%),
                  var(--bg);
      color: var(--text);
      font-family: 'Space Grotesk', 'Fira Sans', 'Avenir Next', 'Helvetica Neue', sans-serif;
    }
    h1, h2, h3, h4, h5 { margin: 0; }
    a { color: var(--info); }
    .hero {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      padding: 20px 24px;
      border: 1px solid var(--border);
      border-radius: 18px;
      background: linear-gradient(135deg, rgba(14,165,233,0.2), rgba(16,185,129,0.18));
      box-shadow: var(--shadow);
    }
    .hero .meta { color: var(--muted); font-size: 14px; }
    .grid { display: grid; gap: 16px; }
    .cols-4 { grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); margin-top: 20px; }
    .cols-2 { grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); margin-top: 18px; }
    .card {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 16px 18px;
      box-shadow: var(--shadow);
    }
    .stat-value { font-size: 28px; font-weight: 700; }
    .stat-label { color: var(--muted); font-size: 13px; }
    .pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 12px;
      border-radius: 999px;
      font-size: 13px;
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--border);
    }
    .pill.pass { color: var(--pass); }
    .pill.fail { color: var(--fail); }
    .pill.skip { color: var(--skip); }
    .chart { width: 100%; height: 320px; }
    .table { width: 100%; border-spacing: 0; border-collapse: collapse; margin-top: 6px; }
    .table thead { background: rgba(255,255,255,0.04); }
    .table th, .table td {
      padding: 10px 12px;
      text-align: left;
      border-bottom: 1px solid var(--border);
      font-size: 13px;
    }
    .table th { color: var(--muted); font-weight: 600; }
    .status-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
    .status-pass { background: var(--pass); }
    .status-fail { background: var(--fail); }
    .status-skip { background: var(--skip); }
    .status-xfailed { background: var(--skip); }
    .status-xpassed { background: #a855f7; }
    .badge {
      display: inline-block;
      padding: 4px 8px;
      background: rgba(255,255,255,0.04);
      border: 1px solid var(--border);
      border-radius: 10px;
      margin-right: 4px;
      color: var(--muted);
      font-size: 12px;
    }
    .insights li { margin-bottom: 6px; color: var(--text); }
    .muted { color: var(--muted); }
    .error-snippet { color: #fecdd3; white-space: pre-wrap; font-family: 'SFMono-Regular', 'JetBrains Mono', monospace; font-size: 12px; }
    .flex { display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }
    .chips { display: flex; gap: 6px; flex-wrap: wrap; }
    .footer { text-align: right; color: var(--muted); margin-top: 12px; font-size: 12px; }
  </style>
</head>
<body>
  <div class="hero">
    <div>
      <div class="pill">Interactive Test Dashboard</div>
      <h1>Run Insights</h1>
      <div class="meta">Generated __CREATED_AT__ • Host __HOSTNAME__</div>
    </div>
    <div class="flex">
      <span class="pill pass">Passed __PASSED__</span>
      <span class="pill fail">Failed __FAILED__</span>
      <span class="pill skip">Skipped __SKIPPED__</span>
    </div>
  </div>

  <div class="grid cols-4">
    <div class="card">
      <div class="stat-value">__EXECUTED__</div>
      <div class="stat-label">Executed tests</div>
    </div>
    <div class="card">
      <div class="stat-value">__PASS_RATE__%</div>
      <div class="stat-label">Pass rate</div>
    </div>
    <div class="card">
      <div class="stat-value">__AVG_DURATION__s</div>
      <div class="stat-label">Avg duration</div>
    </div>
    <div class="card">
      <div class="stat-value">__WALL_CLOCK__s</div>
      <div class="stat-label">Wall clock</div>
    </div>
  </div>

  <div class="grid cols-2">
    <div class="card">
      <h3>Outcome Mix</h3>
      <canvas id="chart-outcome" class="chart"></canvas>
    </div>
    <div class="card">
      <h3>Slowest Tests</h3>
      <canvas id="chart-slowest" class="chart"></canvas>
    </div>
  </div>

  <div class="grid cols-2">
    <div class="card">
      <h3>Insights</h3>
      <ul class="insights">
        __INSIGHTS_HTML__
      </ul>
    </div>
    <div class="card">
      <h3>Markers</h3>
      <div class="chips">
        __MARKERS_HTML__
      </div>
      <h3 style="margin-top:14px;">Files Touched</h3>
      <div class="chips">
        __FILES_HTML__
      </div>
    </div>
  </div>

  <div class="card" style="margin-top:18px;">
    <h3>Detailed Results</h3>
    <table class="table">
      <thead>
        <tr>
          <th>Status</th>
          <th>Test</th>
          <th>File</th>
          <th>Duration</th>
          <th>Markers</th>
          <th>Error / Reason</th>
        </tr>
      </thead>
      <tbody>
        __ROWS_HTML__
      </tbody>
    </table>
    <div class="footer">Python __PYTHON__ • Pytest __PYTEST__ • Browser __BROWSER__</div>
  </div>

  <script>
    const DATA = __DATA__;

    function fmtSeconds(value) {
      if (!value) return '0.00s';
        return value.toFixed(2) + 's';
    function resizeCanvas(canvas, height=320) {
      const ratio = window.devicePixelRatio || 1;
      canvas.width = canvas.clientWidth * ratio;
      canvas.height = height * ratio;
      return ratio;
    }

    function drawDonut(canvasId, slices) {
      const canvas = document.getElementById(canvasId);
      if (!canvas) return;
      const r = resizeCanvas(canvas, 320);
      const ctx = canvas.getContext('2d');
      const total = slices.reduce((s, sl) => s + sl.value, 0) || 1;
      const cx = canvas.width / 2;
      const cy = canvas.height / 2;
      const radius = Math.min(canvas.width, canvas.height) / 2.4;
      let angle = -Math.PI / 2;

      slices.forEach(slice => {
        const delta = (slice.value / total) * Math.PI * 2;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.arc(cx, cy, radius, angle, angle + delta);
        ctx.closePath();
        ctx.fillStyle = slice.color;
        ctx.fill();
        angle += delta;
      });

      ctx.globalCompositeOperation = 'destination-out';
      ctx.beginPath();
      ctx.arc(cx, cy, radius * 0.58, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalCompositeOperation = 'source-over';

      ctx.fillStyle = '#e5e7eb';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.font = (16 * r) + "px 'Space Grotesk', 'Fira Sans', sans-serif";
      const passSlice = slices.find(s => s.key === 'passed');
      const passRate = passSlice ? (passSlice.value / total * 100).toFixed(1) : '0.0';
      ctx.fillText(passRate + '% pass', cx, cy);
    }

    function drawBars(canvasId, labels, values, colors) {
      const canvas = document.getElementById(canvasId);
      if (!canvas) return;
      const r = resizeCanvas(canvas, 320);
      const ctx = canvas.getContext('2d');
      const maxVal = Math.max(...values, 1);
      const padding = 28 * r;
      const availableWidth = canvas.width - padding * 2;
      const barSpace = availableWidth / values.length;
      const barWidth = barSpace * 0.6;
      values.forEach((val, idx) => {
        const height = (val / maxVal) * (canvas.height - padding * 2);
        const x = padding + idx * barSpace + (barSpace - barWidth) / 2;
        const y = canvas.height - padding - height;
        const gradient = ctx.createLinearGradient(0, y, 0, y + height);
        gradient.addColorStop(0, colors[idx] || '#22c55e');
        gradient.addColorStop(1, '#0f172a');
        ctx.fillStyle = gradient;
        ctx.roundRect(x, y, barWidth, height, 8 * r);
        ctx.fill();

        ctx.fillStyle = '#cbd5e1';
        ctx.font = (12 * r) + "px 'Space Grotesk', sans-serif";
        ctx.textAlign = 'center';
        ctx.fillText(labels[idx], x + barWidth / 2, canvas.height - padding / 2);
      });
    }

    if (CanvasRenderingContext2D.prototype.roundRect === undefined) {
      CanvasRenderingContext2D.prototype.roundRect = function (x, y, w, h, r) {
        const min = Math.min(w, h) / 2;
        const radius = Math.min(min, r || 0);
        this.beginPath();
        this.moveTo(x + radius, y);
        this.arcTo(x + w, y, x + w, y + h, radius);
        this.arcTo(x + w, y + h, x, y + h, radius);
        this.arcTo(x, y + h, x, y, radius);
        this.arcTo(x, y, x + w, y, radius);
        this.closePath();
        return this;
      };
    }

    const slices = [
      { key: 'passed', label: 'Passed', value: DATA.summary.counts.passed || 0, color: '#10b981' },
      { key: 'failed', label: 'Failed', value: DATA.summary.counts.failed || 0, color: '#f43f5e' },
      { key: 'skipped', label: 'Skipped', value: DATA.summary.counts.skipped || 0, color: '#fbbf24' },
      { key: 'xfailed', label: 'XFailed', value: DATA.summary.counts.xfailed || 0, color: '#fbbf24' },
      { key: 'xpassed', label: 'XPassed', value: DATA.summary.counts.xpassed || 0, color: '#a855f7' }
    ].filter(s => s.value > 0);

    drawDonut('chart-outcome', slices);

    const slowLabels = DATA.slow_tests.map(t => t.name || t.nodeid);
    const slowValues = DATA.slow_tests.map(t => t.duration || 0);
    const slowColors = slowValues.map((_, idx) => ['#38bdf8', '#f97316', '#10b981', '#f43f5e', '#fbbf24'][idx % 5]);
    drawBars('chart-slowest', slowLabels, slowValues, slowColors);

    window.addEventListener('resize', () => {
      drawDonut('chart-outcome', slices);
      drawBars('chart-slowest', slowLabels, slowValues, slowColors);
    });
  </script>
</body>
</html>"""

        return (
            template
            .replace("__DATA__", data_json)
            .replace("__CREATED_AT__", payload["created_at"])
            .replace("__HOSTNAME__", payload["environment"]["hostname"])
            .replace("__PASSED__", str(passed))
            .replace("__FAILED__", str(failed))
            .replace("__SKIPPED__", str(skipped))
            .replace("__EXECUTED__", str(payload["summary"]["executed"]))
            .replace("__PASS_RATE__", f"{payload['summary']['pass_rate']:.1f}")
            .replace("__AVG_DURATION__", f"{payload['summary']['avg_duration']:.2f}")
            .replace("__WALL_CLOCK__", f"{payload['summary']['wall_clock']:.2f}")
            .replace("__INSIGHTS_HTML__", insights_html)
            .replace("__MARKERS_HTML__", markers_html)
            .replace("__FILES_HTML__", files_html)
            .replace("__ROWS_HTML__", rows_html)
            .replace("__PYTHON__", payload["environment"]["python"])
            .replace("__PYTEST__", payload["environment"]["pytest"])
            .replace("__BROWSER__", payload["environment"]["browser"])
        )

    def _render_row(self, test: Dict[str, Any]) -> str:
        outcome = test.get("outcome", "unknown")
        dot_class = {
            "passed": "status-pass",
            "failed": "status-fail",
            "skipped": "status-skip",
            "xfailed": "status-xfailed",
            "xpassed": "status-xpassed",
        }.get(outcome, "status-skip")

        markers = "".join(f"<span class='badge'>{m}</span>" for m in test.get("keywords", []))
        empty_marker = "<span class='muted'>&mdash;</span>"
        reason = test.get("error") or test.get("reason") or ""
        reason_html = f"<div class='error-snippet'>{reason}</div>" if reason else empty_marker

        return (
            "<tr>"
            f"<td><span class='status-dot {dot_class}'></span> {outcome}</td>"
            f"<td>{test.get('name')}</td>"
            f"<td>{test.get('file')}:{test.get('line')}</td>"
            f"<td>{test.get('duration', 0.0):.2f}s</td>"
            f"<td>{markers or empty_marker}</td>"
            f"<td>{reason_html}</td>"
            "</tr>"
        )

