import os
import pytest
from config.config import Config

@pytest.mark.ui
@pytest.mark.skipif(
    Config.HEADLESS and "CI" in os.environ,
    reason="Skip UI tests in CI environment"
)
def test_demo_site_load(page):
    """Test loading a demo e-commerce site."""
    page.goto("https://demo.nopcommerce.com/")
    assert "nopCommerce" in page.title()
    # Simple validation that page loaded
    assert page.locator(".header-logo").is_visible()