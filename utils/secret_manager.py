#!/usr/bin/env python3
"""
Secret Management and Configuration Validation Utility

This script helps manage secrets and validate configuration for the test framework.
Run this before executing tests to ensure all required secrets are properly configured.

Usage:
    python utils/secret_manager.py validate    # Validate current configuration
    python utils/secret_manager.py mask        # Show masked configuration values
    python utils/secret_manager.py setup       # Interactive setup wizard
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import Config

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class SecretManager:
    """Utility class for managing secrets and configuration validation."""

    REQUIRED_SECRETS = [
        'TEST_USER_EMAIL',
        'TEST_USER_PASSWORD',
    ]

    OPTIONAL_SECRETS = [
        'REQRES_API_KEY',
        'FAKESTORE_API_KEY',
    ]

    SENSITIVE_KEYS = [
        'password', 'secret', 'key', 'token'
    ]

    @classmethod
    def validate_configuration(cls) -> bool:
        """Validate that all required secrets are configured."""
        logger.info("🔍 Validating configuration...")

        missing_required = []
        for secret in cls.REQUIRED_SECRETS:
            value = getattr(Config, secret, '')
            if not value or str(value).startswith('your_'):
                missing_required.append(secret)

        if missing_required:
            logger.error(f"❌ Missing required secrets: {', '.join(missing_required)}")
            logger.info("💡 Set these in your .env file or environment variables")
            return False

        # Check optional secrets
        missing_optional = []
        for secret in cls.OPTIONAL_SECRETS:
            value = getattr(Config, secret, '')
            if not value or str(value).startswith('your_'):
                missing_optional.append(secret)

        if missing_optional:
            logger.warning(f"⚠️  Optional secrets not set: {', '.join(missing_optional)}")
            logger.info("ℹ️  Some tests may be limited without these secrets")

        logger.info("✅ Configuration validation passed")
        return True

    @classmethod
    def show_masked_configuration(cls):
        """Display configuration with sensitive values masked."""
        logger.info("🔒 Current Configuration (sensitive values masked):")
        logger.info("-" * 60)

        config_items = [
            'BASE_URL', 'BROWSER', 'HEADLESS', 'ENVIRONMENT', 'LOG_LEVEL',
            'API_BASE_URL', 'AUTH_API_BASE_URL', 'STORE_API_BASE_URL',
            'TEST_USER_EMAIL', 'INVALID_USER_EMAIL',
            'VALID_USERNAME', 'INVALID_USERNAME',
            'REQRES_API_KEY', 'FAKESTORE_API_KEY',
            'API_TIMEOUT', 'MAX_RETRIES'
        ]

        for item in config_items:
            value = getattr(Config, item, 'NOT_SET')
            masked_value = cls._mask_sensitive_value(item, value)
            logger.info(f"{item:25} : {masked_value}")

        logger.info("-" * 60)

    @classmethod
    def _mask_sensitive_value(cls, key: str, value: any) -> str:
        """Mask sensitive values for display."""
        key_lower = key.lower()

        # Check if key contains sensitive keywords
        if any(sensitive in key_lower for sensitive in cls.SENSITIVE_KEYS):
            if value and str(value) != 'NOT_SET':
                return f"{'*' * 8} (length: {len(str(value))})"
            else:
                return "NOT_SET"

        return str(value)

    @classmethod
    def interactive_setup(cls):
        """Interactive setup wizard for configuration."""
        logger.info("🔧 Interactive Configuration Setup")
        logger.info("This will help you set up your .env file")
        logger.info("-" * 50)

        env_file = Path('.env')
        if env_file.exists():
            response = input("⚠️  .env file already exists. Overwrite? (y/N): ")
            if response.lower() != 'y':
                logger.info("Setup cancelled")
                return

        # Collect configuration values
        config_values = {}

        logger.info("\n📝 Required Secrets:")
        for secret in cls.REQUIRED_SECRETS:
            current_value = getattr(Config, secret, '')
            if current_value and not str(current_value).startswith('your_'):
                use_current = input(f"Use current value for {secret}? (Y/n): ")
                if use_current.lower() in ('', 'y', 'yes'):
                    config_values[secret] = current_value
                    continue

            config_values[secret] = input(f"Enter {secret}: ")

        logger.info("\n📝 Optional Secrets (press Enter to skip):")
        for secret in cls.OPTIONAL_SECRETS:
            current_value = getattr(Config, secret, '')
            if current_value and not str(current_value).startswith('your_'):
                use_current = input(f"Use current value for {secret}? (Y/n): ")
                if use_current.lower() in ('', 'y', 'yes'):
                    config_values[secret] = current_value
                    continue

            value = input(f"Enter {secret} (optional): ")
            if value.strip():
                config_values[secret] = value

        # Write .env file
        with open('.env', 'w') as f:
            f.write("# Environment configuration generated by secret_manager.py\n")
            f.write("# DO NOT commit this file to version control\n\n")

            for key, value in config_values.items():
                f.write(f"{key}={value}\n")

            # Add other default values
            f.write("\n# Default configuration values\n")
            f.write("BASE_URL=https://the-internet.herokuapp.com\n")
            f.write("BROWSER=chromium\n")
            f.write("HEADLESS=true\n")
            f.write("ENVIRONMENT=test\n")
            f.write("LOG_LEVEL=INFO\n")
            f.write("API_TIMEOUT=10\n")
            f.write("MAX_RETRIES=3\n")

        logger.info("✅ Configuration saved to .env file")
        logger.info("🔒 Remember to add .env to your .gitignore!")

def main():
    """Main entry point for the secret manager utility."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == 'validate':
        success = SecretManager.validate_configuration()
        sys.exit(0 if success else 1)

    elif command == 'mask':
        SecretManager.show_masked_configuration()

    elif command == 'setup':
        SecretManager.interactive_setup()

    else:
        logger.error(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)

if __name__ == '__main__':
    main()