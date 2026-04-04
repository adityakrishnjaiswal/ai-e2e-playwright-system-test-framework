#!/bin/bash
# Script to set all environment variables as GitHub repository secrets
# Run this after authenticating with: gh auth login

echo "🔐 Setting up GitHub repository secrets..."

# UI Configuration
echo "https://the-internet.herokuapp.com" | gh secret set BASE_URL
echo "chromium" | gh secret set BROWSER
echo "true" | gh secret set HEADLESS

# API Configuration
echo "https://jsonplaceholder.typicode.com" | gh secret set API_BASE_URL
echo "https://jsonplaceholder.typicode.com" | gh secret set AUTH_API_BASE_URL
echo "https://jsonplaceholder.typicode.com" | gh secret set STORE_API_BASE_URL

# Test Credentials
echo "eve.holt@reqres.in" | gh secret set TEST_USER_EMAIL
echo "cityslicka" | gh secret set TEST_USER_PASSWORD
echo "invalid@example.com" | gh secret set INVALID_USER_EMAIL
echo "wrongpassword" | gh secret set INVALID_USER_PASSWORD

# UI Test Credentials
echo "tomsmith" | gh secret set VALID_USERNAME
echo "SuperSecretPassword!" | gh secret set VALID_PASSWORD
echo "invalid" | gh secret set INVALID_USERNAME
echo "invalid" | gh secret set INVALID_PASSWORD

# API Keys
echo "your_reqres_api_key_here" | gh secret set REQRES_API_KEY
echo "your_fakestore_api_key_here" | gh secret set FAKESTORE_API_KEY

# Environment Settings
echo "test" | gh secret set ENVIRONMENT
echo "INFO" | gh secret set LOG_LEVEL

# Timeouts and Retries
echo "10" | gh secret set API_TIMEOUT
echo "3" | gh secret set MAX_RETRIES

echo "✅ All secrets have been set as GitHub repository secrets!"
echo ""
echo "📋 Secrets set:"
echo "  - BASE_URL, BROWSER, HEADLESS"
echo "  - API_BASE_URL, AUTH_API_BASE_URL, STORE_API_BASE_URL"
echo "  - TEST_USER_EMAIL, TEST_USER_PASSWORD"
echo "  - INVALID_USER_EMAIL, INVALID_USER_PASSWORD"
echo "  - VALID_USERNAME, VALID_PASSWORD"
echo "  - INVALID_USERNAME, INVALID_PASSWORD"
echo "  - REQRES_API_KEY, FAKESTORE_API_KEY"
echo "  - ENVIRONMENT, LOG_LEVEL"
echo "  - API_TIMEOUT, MAX_RETRIES"
echo ""
echo "🔍 You can verify secrets at: https://github.com/adityakrishnjaiswal/ai-e2e-playwright-system-test-framework/settings/secrets/actions"