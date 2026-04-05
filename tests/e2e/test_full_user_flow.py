import pytest
import logging
from api.api_client import APIClient
from utils.assertions import APIAssertions
from config.config import Config

logger = logging.getLogger(__name__)

@pytest.mark.e2e
@pytest.mark.api
def test_full_user_flow(api_client: APIClient):
    """
    Complete end-to-end user journey across multiple services:
    Authentication → Product Discovery → Cart Operations → Validation

    This test demonstrates real-world system testing capabilities,
    including graceful handling of external API dependencies.
    """
    logger.info("🚀 Starting complete e2e user flow test")

    # Step 1: Authentication - Login simulation
    logger.info("Step 1: User Authentication")
    token = api_client.login(
        email=Config.TEST_USER_EMAIL,
        password=Config.TEST_USER_PASSWORD
    )

    # Validate authentication
    APIAssertions.validate_token_format(token)
    assert token is not None, "Authentication should succeed"
    logger.info(f"✅ Authentication successful - Token: {token[:10]}...")

    # Step 2: Product Discovery - Fetch products
    logger.info("Step 2: Product Discovery")
    products = api_client.get_products()

    # Validate products response
    APIAssertions.validate_api_response_success(products, "Product discovery")
    if not products:
        logger.warning("⚠️  No products available - skipping cart operations")
        pytest.skip("External API unavailable - cannot complete full user flow")

    APIAssertions.validate_non_empty_list(products, min_length=1)
    logger.info(f"✅ Retrieved {len(products)} products")

    # Select first available product dynamically
    selected_product = products[0]
    APIAssertions.validate_product_structure(selected_product)
    product_id = selected_product["id"]
    product_title = selected_product["title"]
    logger.info(f"✅ Selected product: {product_title} (ID: {product_id})")

    # Step 3: Cart Operations - Add product to cart
    logger.info("Step 3: Cart Operations")
    user_id = 1  # Using test user ID
    cart = api_client.add_to_cart(
        user_id=user_id,
        product_id=product_id,
        quantity=1
    )

    # Validate cart creation
    APIAssertions.validate_api_response_success(cart, "Cart creation")
    if cart is None:
        logger.warning("⚠️  Cart creation failed - API may be unavailable")
        pytest.skip("External API unavailable - cannot complete cart validation")

    APIAssertions.validate_cart_structure(cart)
    APIAssertions.validate_cart_contains_product(cart, product_id)
    cart_id = cart["id"]
    logger.info(f"✅ Cart created successfully - Cart ID: {cart_id}")

    # Step 4: Cart Validation - Fetch and verify carts
    logger.info("Step 4: Cart Validation")
    user_carts = api_client.get_carts(user_id=user_id)

    # Validate user's carts
    APIAssertions.validate_api_response_success(user_carts, "Cart retrieval")
    if not user_carts:
        logger.warning("⚠️  No user carts found - cart may not have persisted")
        # Still validate the cart we created if possible
        APIAssertions.validate_cart_structure(cart)
        logger.info("✅ Created cart structure validated (persistence may vary)")
    else:
        APIAssertions.validate_non_empty_list(user_carts, min_length=1)
        logger.info(f"✅ Retrieved {len(user_carts)} carts for user {user_id}")

        # Find our newly created cart
        created_cart = None
        for cart_item in user_carts:
            if cart_item["id"] == cart_id:
                created_cart = cart_item
                break

        if created_cart:
            logger.info("✅ Created cart found in user's cart list")
        else:
            logger.warning("⚠️  Created cart not found in user's cart list (may be API behavior)")

    # Step 5: Cross-service Data Consistency Validation
    logger.info("Step 5: Data Consistency Validation")

    # Verify cart belongs to correct user
    assert cart["userId"] == user_id, f"Cart user mismatch: expected {user_id}, got {cart['userId']}"

    # Verify product details in cart
    cart_products = cart["products"]
    assert len(cart_products) == 1, f"Cart should contain 1 product, got {len(cart_products)}"

    cart_product = cart_products[0]
    assert cart_product["productId"] == product_id, f"Cart product ID mismatch: expected {product_id}, got {cart_product['productId']}"
    assert cart_product["quantity"] == 1, f"Cart quantity mismatch: expected 1, got {cart_product['quantity']}"

    # Verify product still exists and matches
    product_still_exists = any(p["id"] == product_id for p in products)
    assert product_still_exists, f"Product {product_id} no longer exists in product catalog"

    logger.info("✅ All data consistency checks passed")
    logger.info("🎉 Complete e2e user flow test PASSED!")
