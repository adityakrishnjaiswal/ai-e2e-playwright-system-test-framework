# AI-Driven End-to-End Test Automation Framework

[![CI](https://github.com/your-repo/ai-e2e-playwright-system-test-framework/actions/workflows/ci.yml/badge.svg)](https://github.com/your-repo/ai-e2e-playwright-system-test-framework/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.40+-green.svg)](https://playwright.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-7.4+-red.svg)](https://pytest.org/)

A production-ready, scalable end-to-end test automation framework built with Python, Playwright, Pytest, and API testing. Designed for modern software teams seeking reliable, maintainable, and AI-enhanced test automation.

## 🎯 Problem Statement

Modern software development faces significant challenges with test automation:

- **Flaky Tests**: Unreliable UI tests causing false positives and eroded team confidence
- **Slow Release Cycles**: Manual testing bottlenecks and inefficient automation
- **Maintenance Overhead**: Brittle test code requiring constant updates
- **Limited Coverage**: Siloed testing approaches missing critical integration points
- **Scalability Issues**: Tests that work locally but fail in CI/CD pipelines

## 🚀 Solution

This framework provides a comprehensive testing solution that:

- Combines UI, API, and end-to-end testing in a single, cohesive system
- Implements industry best practices with Page Object Model and API client patterns
- Includes AI-assisted utilities for intelligent test data generation
- Ensures CI/CD reliability with headless execution and parallel test runs
- Provides rich reporting and artifact generation for better insights

## ✨ Features

### Core Testing Capabilities
- **UI Automation**: Playwright-based browser automation with cross-browser support
- **API Testing**: RESTful API validation with request/response handling
- **End-to-End Flows**: Integrated testing scenarios combining UI and API interactions
- **Parallel Execution**: Distributed test runs using pytest-xdist for faster feedback

### AI-Enhanced Features
- **Dynamic Test Data Generation**: Intelligent creation of realistic test data
- **Smart Assertions**: Enhanced validation with contextual error reporting

### Developer Experience
- **Page Object Model**: Maintainable UI test structure
- **Fixture Management**: Efficient test setup and teardown
- **Comprehensive Reporting**: HTML reports with screenshots and logs
- **Environment Configuration**: Flexible configuration via environment variables

### CI/CD Integration
- **GitHub Actions**: Pre-configured CI pipeline
- **Artifact Upload**: Test reports and screenshots preservation
- **Conditional Execution**: Smart test skipping based on environment

## 🏗️ Architecture

```
├── config/           # Configuration management
├── pages/            # Page Object Model classes
├── api/              # API client and utilities
├── utils/            # AI-assisted utilities
├── tests/            # Test suites
│   ├── ui/          # UI test cases
│   ├── api/         # API test cases
│   └── e2e/         # End-to-end scenarios
├── reports/          # Test execution reports
└── .github/          # CI/CD workflows
```

### Key Components

- **Config Module**: Centralized configuration with environment variable support
- **Page Objects**: Encapsulated UI interactions for maintainability
- **API Client**: HTTP client with authentication and session management
- **Test Data Generator**: AI-powered realistic data creation
- **Pytest Fixtures**: Shared test resources and setup

## 📋 Prerequisites

- Python 3.9+
- Node.js (for Playwright browser installation)
- Git

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo/ai-e2e-playwright-system-test-framework.git
   cd ai-e2e-playwright-system-test-framework
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```bash
   playwright install
   ```

## 🔐 Security Configuration

### Environment Variables

The framework uses environment variables for all sensitive configuration to follow security best practices:

| Variable | Description | Required |
|----------|-------------|----------|
| `TEST_USER_EMAIL` | Test user email for authentication | ✅ |
| `TEST_USER_PASSWORD` | Test user password | ✅ |
| `REQRES_API_KEY` | API key for ReqRes service | ❌ |
| `FAKESTORE_API_KEY` | API key for FakeStore API | ❌ |
| `BASE_URL` | Base URL for UI tests | ✅ |
| `API_BASE_URL` | Base API endpoint | ✅ |
| `AUTH_API_BASE_URL` | Authentication API endpoint | ✅ |
| `STORE_API_BASE_URL` | Store API endpoint | ✅ |
| `BROWSER` | Browser for Playwright (chromium/firefox/webkit) | ✅ |
| `HEADLESS` | Run browser in headless mode | ✅ |
| `ENVIRONMENT` | Test environment (test/staging/prod) | ✅ |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | ✅ |
| `API_TIMEOUT` | API request timeout in seconds | ✅ |
| `MAX_RETRIES` | Maximum retry attempts for failed requests | ✅ |

### Secret Management Utility

Use the built-in secret manager for secure configuration:

```bash
# Validate current configuration
python utils/secret_manager.py validate

# Show masked configuration (safe for sharing)
python utils/secret_manager.py mask

# Interactive setup wizard
python utils/secret_manager.py setup
```

### Security Best Practices Implemented

- ✅ **No Hardcoded Secrets**: All credentials externalized to environment variables
- ✅ **Masked Logging**: Sensitive data automatically masked in logs
- ✅ **Configuration Validation**: Required secrets validated on startup
- ✅ **Environment-Specific Config**: Support for multiple deployment environments
- ✅ **Git-Safe**: `.env` files excluded from version control
- ✅ **CI/CD Ready**: Secrets can be injected via secure pipelines

### Configuration Setup

1. **Copy environment template**
   ```bash
   cp .env.example .env
   ```

2. **Edit with your values**
   ```bash
   # Required secrets
   TEST_USER_EMAIL=your-test-user@example.com
   TEST_USER_PASSWORD=your-secure-password

   # Optional API keys
   REQRES_API_KEY=your-reqres-api-key
   FAKESTORE_API_KEY=your-fakestore-api-key
   ```

3. **Validate configuration**
   ```bash
   python utils/secret_manager.py validate
   ```

## 🧪 Running Tests

### Pre-Flight Checks
```bash
# Always validate configuration before running tests
python utils/secret_manager.py validate
```

### Run All Tests
```bash
pytest
```

### Run Specific Test Types
```bash
# API tests only
pytest -m api

# UI tests only
pytest -m ui

# End-to-end tests
pytest -m e2e
```

### Run with Parallel Execution
```bash
pytest -n auto
```

### Generate HTML Report
```bash
pytest --html=reports/report.html --self-contained-html
```

### Run in Headless Mode
```bash
HEADLESS=true pytest
```

## 🔄 CI/CD Pipeline

The framework includes a GitHub Actions workflow that:

1. **Security Validation**: Validates all required secrets are configured
2. Sets up Python environment
3. Installs dependencies and Playwright browsers
4. Runs smoke tests for basic validation
5. Executes API, UI, and E2E test suites
6. Generates and uploads test reports

### Pipeline Stages
- **Security Check**: `python utils/secret_manager.py validate`
- **Setup**: Environment preparation
- **Smoke Test**: Basic functionality validation
- **API Tests**: Backend service validation
- **UI Tests**: Frontend interaction testing
- **E2E Tests**: Complete workflow validation
- **Reporting**: Artifact generation and upload

### Example CI Configuration
```yaml
- name: Validate Secrets
  run: python utils/secret_manager.py validate

- name: Run Tests
  run: pytest --html=reports/test_report.html --junitxml=reports/junit.xml
  env:
    TEST_USER_EMAIL: ${{ secrets.TEST_USER_EMAIL }}
    TEST_USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}
```

## 📊 Test Reporting

Tests generate comprehensive HTML reports including:
- Test execution summary
- Pass/fail status with timestamps
- Screenshots for UI test failures
- Detailed error logs and stack traces
- Performance metrics

Reports are automatically saved to the `reports/` directory.

## 🤖 AI Features

### Dynamic Test Data Generator
Generate realistic test data for various scenarios:

```python
from utils.test_data_generator import TestDataGenerator

# Generate single user
user = TestDataGenerator.generate_user()
# {'email': 'test123@example.com', 'password': 'Abc123!@#', ...}

# Generate multiple users
users = TestDataGenerator.generate_users(5)
```

## 🔄 End-to-End System Testing

This framework validates a complete user journey across multiple services, demonstrating real-world system testing capabilities beyond isolated UI/API testing.

### Complete User Flow Test (`tests/e2e/test_full_user_flow.py`)

**Scenario**: Full e-commerce user journey from authentication to cart validation

1. **Authentication Service** (ReqRes API)
   - POST `https://reqres.in/api/login`
   - Email: `eve.holt@reqres.in`
   - Password: `cityslicka`
   - **Validates**: Token extraction and format

2. **Product Service** (FakeStore API)
   - GET `https://fakestoreapi.com/products`
   - **Validates**: Product catalog retrieval and structure

3. **Cart Service** (FakeStore API)
   - POST `https://fakestoreapi.com/carts`
   - **Validates**: Cart creation with product association

4. **Cart Validation** (FakeStore API)
   - GET `https://fakestoreapi.com/carts`
   - **Validates**: Cart persistence and data consistency

### Key Testing Capabilities Demonstrated

- **Multi-Service Integration**: Testing across authentication, product, and cart services
- **Cross-Service Data Flow**: Validating data consistency between different APIs
- **Real-World API Behavior**: Handling actual HTTP responses and error conditions
- **System-Level Validation**: Ensuring end-to-end business logic correctness
- **Distributed System Testing**: Simulating real user interactions across microservices

### Negative Testing Scenarios (`tests/e2e/test_negative_flow.py`)

- **Invalid Authentication**: Testing failed login attempts
- **Empty Cart Handling**: Validating cart operations with invalid data
- **Non-existent Resources**: Testing API behavior with invalid product/user IDs
- **Malformed Requests**: Edge case handling and error recovery

### API Client Architecture

The enhanced `api/api_client.py` provides:

- **Real API Integration**: Direct calls to ReqRes and FakeStore APIs
- **Comprehensive Error Handling**: Request timeouts, status code validation, exception handling
- **Detailed Logging**: Step-by-step execution tracking for debugging
- **Response Validation**: Automatic status code and data structure checks
- **Session Management**: Efficient HTTP connection reuse

### Assertion Layer (`utils/assertions.py`)

Reusable validation utilities:
- `validate_response_status()`: HTTP status code validation
- `validate_non_empty_list()`: List content validation
- `validate_key_exists()`: JSON structure validation
- `validate_product_structure()`: Product data schema validation
- `validate_cart_structure()`: Cart data schema validation

This demonstrates enterprise-grade testing practices with modular, maintainable assertion logic.

## 🧪 Example Test Cases

### API Test
```python
@pytest.mark.api
def test_login_success(api_client):
    response = api_client.login("user@example.com", "password")
    assert response.status_code == 200
    assert 'token' in response.json()
```

### UI Test
```python
@pytest.mark.ui
def test_login_success(page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("username", "password")
    assert "Login successful" in login_page.get_flash_message()
```

### End-to-End Test
```python
@pytest.mark.e2e
def test_complete_workflow(api_client, page):
    # API login
    api_client.login("user@example.com", "password")
    # UI interaction
    dashboard = DashboardPage(page)
    dashboard.navigate()
    assert dashboard.is_logged_in()
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation as needed
- Ensure CI pipeline passes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Playwright](https://playwright.dev/) for reliable browser automation
- [Pytest](https://pytest.org/) for comprehensive testing framework
- [ReqRes](https://reqres.in/) for API testing examples
- [The Internet](https://the-internet.herokuapp.com/) for UI testing playground

---

**Built with ❤️ for the testing community**