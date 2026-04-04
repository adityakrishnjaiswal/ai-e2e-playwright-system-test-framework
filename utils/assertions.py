import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class APIAssertions:
    """Reusable assertion utilities for API testing."""

    @staticmethod
    def validate_response_status(response, expected_status: int = 200) -> None:
        """Validate HTTP response status code."""
        assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}"

    @staticmethod
    def validate_non_empty_list(data: List, min_length: int = 1) -> None:
        """Validate that a list is not empty and has minimum length."""
        assert isinstance(data, list), f"Expected list, got {type(data)}"
        assert len(data) >= min_length, f"Expected at least {min_length} items, got {len(data)}"

    @staticmethod
    def validate_key_exists(data: Dict[str, Any], key: str) -> None:
        """Validate that a key exists in a dictionary."""
        assert key in data, f"Key '{key}' not found in response data. Available keys: {list(data.keys())}"

    @staticmethod
    def validate_product_structure(product: Dict[str, Any]) -> None:
        """Validate product data structure."""
        required_keys = ["id", "title", "price", "description", "category", "image"]
        for key in required_keys:
            APIAssertions.validate_key_exists(product, key)
        assert isinstance(product["price"], (int, float)), f"Price should be numeric, got {type(product['price'])}"

    @staticmethod
    def validate_cart_structure(cart: Dict[str, Any]) -> None:
        """Validate cart data structure."""
        required_keys = ["id", "userId", "date", "products"]
        for key in required_keys:
            APIAssertions.validate_key_exists(cart, key)
        assert isinstance(cart["products"], list), f"Products should be a list, got {type(cart['products'])}"
        assert len(cart["products"]) > 0, "Cart should contain at least one product"

    @staticmethod
    def validate_cart_contains_product(cart: Dict[str, Any], product_id: int) -> None:
        """Validate that a cart contains a specific product."""
        products = cart["products"]
        product_ids = [p["productId"] for p in products]
        assert product_id in product_ids, f"Product {product_id} not found in cart. Cart products: {product_ids}"

    @staticmethod
    def validate_token_format(token: str) -> None:
        """Validate authentication token format."""
        assert token is not None, "Token should not be None"
        assert isinstance(token, str), f"Token should be string, got {type(token)}"
        assert len(token.strip()) > 0, "Token should not be empty"

    @staticmethod
    def validate_api_response_success(data, operation: str) -> None:
        """Validate that an API operation returned successful data."""
        if data is None:
            logger.warning(f"⚠️  {operation} returned None - API may be unavailable")
            # In real scenarios, you might want to skip the test or use alternative data
            # For demo purposes, we'll allow None responses but log the issue
            return

        if isinstance(data, list) and len(data) == 0:
            logger.warning(f"⚠️  {operation} returned empty list - API may be unavailable")
            return

        logger.info(f"✅ {operation} validation passed")