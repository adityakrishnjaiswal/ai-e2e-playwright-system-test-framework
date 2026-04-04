import pytest
from api.api_client import APIClient

@pytest.mark.e2e
def test_user_journey(api_client: APIClient):
    """Complete end-to-end user journey: browse products → add to cart → validate cart."""

    # Note: Authentication step skipped due to ReqRes API key requirements
    # In a real system, this would authenticate the user

    # Step 1: Get products (simulating product discovery)
    products = api_client.get_products()
    assert len(products) > 0, "Should retrieve products"
    assert "id" in products[0], "Products should have id"
    assert "title" in products[0], "Products should have title"
    assert "body" in products[0], "Products should have body"

    product_id = products[0]["id"]

    # Step 2: Add to cart (simulating cart operation)
    cart = api_client.add_to_cart(user_id=1, product_id=product_id)
    assert cart is not None, "Cart creation should succeed"
    assert "id" in cart, "Cart should have id"
    assert "title" in cart, "Cart should have title"
    assert cart["userId"] == 1, "Cart should be associated with correct user"
    assert str(product_id) in cart["body"], "Cart should contain the product reference"

    # Step 3: Validate cart (get all carts and verify structure)
    carts = api_client.get_carts()
    assert len(carts) > 0, "Should retrieve carts"
    # Verify cart structure
    cart_item = carts[-1]  # Check the last cart (most recent)
    assert "id" in cart_item, "Cart should have id"
    assert "userId" in cart_item, "Cart should have userId"
    assert "title" in cart_item, "Cart should have title"
    assert "body" in cart_item, "Cart should have body"