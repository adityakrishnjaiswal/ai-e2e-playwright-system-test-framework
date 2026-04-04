import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the test framework."""

    # UI Configuration
    BASE_URL = os.getenv('BASE_URL', 'https://the-internet.herokuapp.com')
    BROWSER = os.getenv('BROWSER', 'chromium')
    HEADLESS = os.getenv('HEADLESS', 'true').lower() == 'true'

    # API Configuration
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://jsonplaceholder.typicode.com')

    # Test Data
    VALID_USERNAME = 'tomsmith'
    VALID_PASSWORD = 'SuperSecretPassword!'
    INVALID_USERNAME = 'invalid'
    INVALID_PASSWORD = 'invalid'