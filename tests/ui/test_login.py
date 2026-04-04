import pytest
from pages.login_page import LoginPage
from config.config import Config

@pytest.mark.ui
def test_login_success(page):
    """Test successful login on UI."""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(Config.VALID_USERNAME, Config.VALID_PASSWORD)
    message = login_page.get_flash_message()
    assert "You logged into a secure area!" in message

@pytest.mark.ui
def test_login_invalid_username(page):
    """Test login with invalid username."""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(Config.INVALID_USERNAME, Config.VALID_PASSWORD)
    message = login_page.get_flash_message()
    assert "Your username is invalid!" in message

@pytest.mark.ui
def test_login_invalid_password(page):
    """Test login with invalid password."""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(Config.VALID_USERNAME, Config.INVALID_PASSWORD)
    message = login_page.get_flash_message()
    assert "Your password is invalid!" in message