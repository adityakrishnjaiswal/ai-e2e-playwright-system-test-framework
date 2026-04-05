import os
import pytest
import logging
from pathlib import Path
from playwright.sync_api import Playwright, Browser, Page
from playwright._impl._api_types import Error as PlaywrightError
from config.config import Config
from api.api_client import APIClient

# Register custom rich HTML dashboard reporter
pytest_plugins = ["utils.custom_reporter"]

pytest_plugins = ["utils.custom_reporter"]

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session", autouse=True)
def validate_secrets():
    """Validate that all required secrets are configured before running tests."""
    try:
        Config.validate_required_secrets()
        logger.info("✅ Secret validation passed")
    except ValueError as e:
        logger.error(f"❌ Secret validation failed: {e}")
        pytest.exit(f"Missing required configuration: {e}", 1)

@pytest.fixture(scope="session")
def playwright_browser(playwright: Playwright) -> Browser:
    """Launch browser for the session."""
    launch_kwargs = {"headless": Config.HEADLESS}

    # Prefer a system Chrome if present to avoid quarantined bundled builds.
    if Config.BROWSER == "chromium":
        system_chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        custom_chrome = os.getenv("PLAYWRIGHT_CHROMIUM_PATH")
        if custom_chrome and Path(custom_chrome).exists():
            launch_kwargs["executable_path"] = custom_chrome
        elif system_chrome.exists():
            launch_kwargs["executable_path"] = str(system_chrome)

    try:
        browser = playwright[Config.BROWSER].launch(**launch_kwargs)
    except PlaywrightError as exc:
        pytest.skip(f"Browser launch failed: {exc}")
    except Exception as exc:  # pragma: no cover - fallback path
        pytest.skip(f"Browser launch failed: {exc}")
    yield browser
    browser.close()

@pytest.fixture
def page(playwright_browser: Browser) -> Page:
    """Create a new page for each test."""
    page = playwright_browser.new_page()
    yield page
    page.close()

@pytest.fixture(scope="session")
def api_client() -> APIClient:
    """API client fixture for e-commerce testing."""
    return APIClient()
