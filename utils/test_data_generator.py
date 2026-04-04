import random
import string
from typing import Dict, Any

class TestDataGenerator:
    """AI-assisted test data generator for dynamic test data creation."""

    @staticmethod
    def generate_email() -> str:
        """Generate a random email address."""
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        domain = random.choice(['test.com', 'example.com', 'demo.com'])
        return f"{username}@{domain}"

    @staticmethod
    def generate_password(length: int = 12) -> str:
        """Generate a random password."""
        chars = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choices(chars, k=length))

    @staticmethod
    def generate_user() -> Dict[str, str]:
        """Generate a complete user data dictionary."""
        return {
            'email': TestDataGenerator.generate_email(),
            'password': TestDataGenerator.generate_password(),
            'first_name': ''.join(random.choices(string.ascii_letters, k=6)).capitalize(),
            'last_name': ''.join(random.choices(string.ascii_letters, k=6)).capitalize()
        }

    @staticmethod
    def generate_users(count: int) -> list:
        """Generate a list of user data."""
        return [TestDataGenerator.generate_user() for _ in range(count)]