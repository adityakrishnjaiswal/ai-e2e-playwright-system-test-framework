from playwright.sync_api import Page
from config.config import Config

class LoginPage:
    """Page Object for the login page."""

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("button[type='submit']")
        self.flash_message = page.locator("#flash")

    def navigate(self):
        """Navigate to the login page."""
        self.page.goto(f"{Config.BASE_URL}/login")

    def login(self, username: str, password: str):
        """Perform login with given credentials."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_flash_message(self) -> str:
        """Get the flash message text."""
        return self.flash_message.text_content().strip()