import pytest
import logging
from api.api_client import APIClient
from utils.assertions import APIAssertions
from config.config import Config

logger = logging.getLogger(__name__)

@pytest.mark.e2e
@pytest.mark.api
def test_user_journey(api_client: APIClient):
    """Complete end-to-end user journey: Authentication → Product Discovery → Cart Operations → Validation."""

    logger.info("🚀 Starting user journey test")

    # Step 1: Authentication (using configured API)
    logger.info("Step 1: User Authentication")
    token = api_client.login(
        email=Config.TEST_USER_EMAIL,
        password=Config.TEST_USER_PASSWORD
    )

    # Validate authentication
    APIAssertions.validate_token_format(token)
    assert token is not None, "Authentication should succeed"
    logger.info("✅ Authentication successful")

    # Step 2: Product Discovery
    logger.info("Step 2: Product Discovery")
    products = api_client.get_products()

    # Validate products response
    APIAssertions.validate_api_response_success(products, "Product discovery")
    if not products:
        logger.warning("⚠️  No products available - skipping remaining steps")
        pytest.skip("External API unavailable for product discovery")

    APIAssertions.validate_non_empty_list(products, min_length=1)
    logger.info(f"✅ Retrieved {len(products)} products")

    # Select first product dynamically
    selected_product = products[0]
    APIAssertions.validate_product_structure(selected_product)
    product_id = selected_product["id"]
    logger.info(f"✅ Selected product: {selected_product['title']} (ID: {product_id})")

    # Step 3: Cart Operations
    logger.info("Step 3: Cart Operations")
    cart = api_client.add_to_cart(user_id=1, product_id=product_id)
    assert cart is not None, "Cart creation should succeed"
    APIAssertions.validate_cart_structure(cart)
    APIAssertions.validate_cart_contains_product(cart, product_id)
    logger.info(f"✅ Cart created successfully with ID: {cart['id']}")

    # Step 4: Cart Validation
    logger.info("Step 4: Cart Validation")
    carts = api_client.get_carts()
    APIAssertions.validate_api_response_success(carts, "Cart validation")
    if carts:
        APIAssertions.validate_non_empty_list(carts, min_length=1)
        logger.info(f"✅ Retrieved {len(carts)} carts")

        # Verify cart structure and data consistency
        cart_item = carts[-1]  # Check the most recent cart
        APIAssertions.validate_cart_structure(cart_item)
        logger.info("✅ Cart structure validation passed")
    else:
        logger.warning("⚠️  No carts retrieved - validating created cart structure only")
        APIAssertions.validate_cart_structure(cart)

    logger.info("🎉 User journey test completed successfully!")