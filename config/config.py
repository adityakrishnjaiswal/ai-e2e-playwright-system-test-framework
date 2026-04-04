import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the test framework with secure secret management."""

    # UI Configuration
    BASE_URL = os.getenv('BASE_URL', 'https://the-internet.herokuapp.com')
    BROWSER = os.getenv('BROWSER', 'chromium')
    HEADLESS = os.getenv('HEADLESS', 'true').lower() == 'true'

    # API Configuration - External Services
    API_BASE_URL = os.getenv('API_BASE_URL', 'https://jsonplaceholder.typicode.com')
    AUTH_API_BASE_URL = os.getenv('AUTH_API_BASE_URL', 'https://jsonplaceholder.typicode.com')
    STORE_API_BASE_URL = os.getenv('STORE_API_BASE_URL', 'https://jsonplaceholder.typicode.com')

    # Test Credentials - Should be stored in secure vault/environment
    TEST_USER_EMAIL = os.getenv('TEST_USER_EMAIL', 'eve.holt@reqres.in')
    TEST_USER_PASSWORD = os.getenv('TEST_USER_PASSWORD', 'cityslicka')
    INVALID_USER_EMAIL = os.getenv('INVALID_USER_EMAIL', 'invalid@example.com')
    INVALID_USER_PASSWORD = os.getenv('INVALID_USER_PASSWORD', 'wrongpassword')

    # UI Test Credentials
    VALID_USERNAME = os.getenv('VALID_USERNAME', 'tomsmith')
    VALID_PASSWORD = os.getenv('VALID_PASSWORD', 'SuperSecretPassword!')
    INVALID_USERNAME = os.getenv('INVALID_USERNAME', 'invalid')
    INVALID_PASSWORD = os.getenv('INVALID_PASSWORD', 'invalid')

    # API Keys and Tokens (for services that require them)
    REQRES_API_KEY = os.getenv('REQRES_API_KEY', '')  # Optional - ReqRes may require this
    FAKESTORE_API_KEY = os.getenv('FAKESTORE_API_KEY', '')  # Optional

    # Test Environment Settings
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'test')  # dev, test, staging, prod
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # Timeouts and Retry Settings
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', '10'))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))

    @classmethod
    def validate_required_secrets(cls):
        """Validate that all required secrets are present."""
        required_secrets = [
            'TEST_USER_EMAIL',
            'TEST_USER_PASSWORD',
        ]

        missing_secrets = []
        for secret in required_secrets:
            value = getattr(cls, secret)
            if not value or value.startswith('your_'):
                missing_secrets.append(secret)

        if missing_secrets:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_secrets)}")

        # Log warning for optional but recommended secrets
        optional_secrets = ['REQRES_API_KEY', 'FAKESTORE_API_KEY']
        for secret in optional_secrets:
            if not getattr(cls, secret):
                print(f"WARNING: Optional secret {secret} not set. Some tests may be limited.")

    @classmethod
    def get_masked_value(cls, key: str) -> str:
        """Get a configuration value with sensitive data masked."""
        value = getattr(cls, key, '')
        if 'password' in key.lower() or 'secret' in key.lower() or 'key' in key.lower():
            return f"{'*' * 8} (length: {len(value)})" if value else "NOT SET"
        return value
    INVALID_PASSWORD = 'invalid'