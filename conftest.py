import pytest
from playwright.sync_api import Playwright, Browser, Page
from config.config import Config
from api.api_client import APIClient

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