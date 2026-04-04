#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${1:-.env}"
REPO="${2:-}"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE" >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "GitHub CLI not authenticated; run gh auth login" >&2
  exit 1
fi

# If no repo provided, derive from current directory (works when inside a git repo)
if [[ -z "$REPO" ]]; then
  REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)
fi

REPO_ARG=()
[[ -n "$REPO" ]] && REPO_ARG=(--repo "$REPO")

while IFS= read -r line || [[ -n "$line" ]]; do
  # trim whitespace
  trimmed="${line#${line%%[![:space:]]*}}"
  trimmed="${trimmed%${trimmed##*[![:space:]]}}"
  [[ -z "$trimmed" ]] && continue
  [[ "$trimmed" =~ ^# ]] && continue
  if [[ "$trimmed" != *"="* ]]; then
    echo "Skip (no '='): $trimmed" >&2
    continue
  fi
  key="${trimmed%%=*}"
  val="${trimmed#*=}"
  key="$(echo "$key" | xargs)"
  val="${val#${val%%[![:space:]]*}}"
  val="${val%${val##*[![:space:]]}}"
  # strip surrounding quotes
  if [[ "$val" =~ ^\".*\"$ ]]; then
    val="${val:1:-1}"
  elif [[ "$val" =~ ^\'.*\'$ ]]; then
    val="${val:1:-1}"
  fi
  [[ -z "$key" ]] && continue
  echo "Setting $key"
  gh secret set "$key" "${REPO_ARG[@]}" --body "$val"
done < "$ENV_FILE"
