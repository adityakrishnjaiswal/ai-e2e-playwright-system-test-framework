from playwright.sync_api import Page, Locator
from config.config import Config

class LoginPage:
    """Page Object for the login page."""

    def __init__(self, page: Page):
        self.page: Page = page
        self.username_input: Locator = page.locator("#username")
        self.password_input: Locator = page.locator("#password")
        self.login_button: Locator = page.locator("button[type='submit']")
        self.flash_message: Locator = page.locator("#flash")

    def navigate(self):
        """Navigate to the login page."""
        self.page.goto(f"{Config.BASE_URL}/login", wait_until="domcontentloaded")
        self.page.wait_for_load_state("networkidle")

    def login(self, username: str, password: str):
        """Perform login with given credentials."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        # UI occasionally lags on slower runners; wait explicitly for feedback.
        self.flash_message.wait_for(state="visible", timeout=5_000)

    def get_flash_message(self) -> str:
        """Get the flash message text."""
        message = self.flash_message.text_content() or ""
        return message.strip()
