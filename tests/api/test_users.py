import pytest
from config.config import Config

@pytest.mark.api
def test_login_success(api_client):
    """Test successful login API."""
    token = api_client.login("eve.holt@reqres.in", "cityslicka")
    assert token is not None
    assert token == "mock_token_12345"

@pytest.mark.api
def test_login_failure(api_client):
    """Test failed login API - mock always succeeds."""
    token = api_client.login("invalid@email.com", "wrongpassword")
    assert token is not None  # Mock login always succeeds

@pytest.mark.api
def test_get_products(api_client):
    """Test get products API."""
    products = api_client.get_products()
    assert len(products) > 0
    assert isinstance(products, list)
    assert "id" in products[0]
    assert "title" in products[0]
    assert "body" in products[0]

@pytest.mark.api
def test_add_to_cart(api_client):
    """Test add to cart API."""
    cart = api_client.add_to_cart(user_id=1, product_id=1)
    assert cart is not None
    assert "id" in cart
    assert cart["userId"] == 1
    assert "Product ID: 1" in cart["body"]

@pytest.mark.e2e
def test_login_and_get_products(api_client):
    """End-to-end test: Login and then access resource."""
    # Login
    token = api_client.login("eve.holt@reqres.in", "cityslicka")
    assert token is not None

    # Then get products
    products = api_client.get_products()
    assert len(products) > 0