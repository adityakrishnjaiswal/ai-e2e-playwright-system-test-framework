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

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
# UI Configuration
BASE_URL=https://the-internet.herokuapp.com
BROWSER=chromium
HEADLESS=true

# API Configuration
API_BASE_URL=https://reqres.in

# Test Credentials
VALID_USERNAME=tomsmith
VALID_PASSWORD=SuperSecretPassword!
```

## 🧪 Running Tests

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

1. Sets up Python environment
2. Installs dependencies and Playwright browsers
3. Runs smoke tests for basic validation
4. Executes API, UI, and E2E test suites
5. Generates and uploads test reports

### Pipeline Stages
- **Setup**: Environment preparation
- **Smoke Test**: Basic functionality validation
- **API Tests**: Backend service validation
- **UI Tests**: Frontend interaction testing
- **E2E Tests**: Complete workflow validation
- **Reporting**: Artifact generation and upload

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

## 🔄 End-to-End Workflow

This framework validates a complete user journey simulating a real-world e-commerce system:

### User Journey Test (`tests/e2e/test_user_journey.py`)
1. **Authentication**: Login using ReqRes API
   - POST https://reqres.in/api/login
   - Validates token generation

2. **Product Discovery**: Retrieve products from FakeStore API
   - GET https://fakestoreapi.com/products
   - Validates product data structure

3. **Cart Operations**: Add products to cart
   - POST https://fakestoreapi.com/carts
   - Creates cart with user and product association

4. **Cart Validation**: Verify cart contents
   - GET https://fakestoreapi.com/carts
   - Confirms cart persistence and data integrity

This end-to-end flow demonstrates:
- **Multi-API Integration**: Testing across different services
- **Data Flow Validation**: Ensuring data consistency between systems
- **Real-world Scenarios**: Simulating actual user behavior
- **System Reliability**: Validating complete business workflows

### API Client Architecture
- **Modular Design**: Separate clients for auth and store APIs
- **Error Handling**: Comprehensive exception handling and logging
- **Session Management**: Persistent HTTP sessions for efficiency
- **Type Safety**: Full type hints for better code maintainability

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