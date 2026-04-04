import pytest
import logging
from playwright.sync_api import Playwright, Browser, Page
from config.config import Config
from api.api_client import APIClient

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
    browser = playwright[Config.BROWSER].launch(headless=Config.HEADLESS)
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