import requests
import logging
from typing import Dict, Any, Optional, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIClient:
    """API client for e-commerce system testing with authentication, products, and cart operations."""

    def __init__(self, base_url: str = "https://jsonplaceholder.typicode.com"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def login(self, email: str, password: str) -> Optional[str]:
        """Login simulation - returns a mock token for demo purposes."""
        # Note: ReqRes API now requires API key, so using mock token for demo
        logger.info(f"Simulating login for user: {email}")
        self.token = "mock_token_12345"
        logger.info("Mock login successful")
        return self.token

    def get_products(self) -> List[Dict[str, Any]]:
        """Get list of posts (simulating products)."""
        try:
            url = f"{self.base_url}/posts"
            logger.info("Fetching products (posts)")
            response = self.session.get(url, timeout=10)

            if response.status_code == 200:
                products = response.json()
                logger.info(f"Retrieved {len(products)} products")
                return products
            else:
                logger.error(f"Failed to get products: {response.status_code}")
                return []
        except requests.RequestException as e:
            logger.error(f"Get products request failed: {e}")
            return []

    def add_to_cart(self, user_id: int, product_id: int) -> Optional[Dict[str, Any]]:
        """Add product to cart by creating a post (simulating cart)."""
        try:
            url = f"{self.base_url}/posts"
            payload = {
                "title": f"Cart for user {user_id}",
                "body": f"Product ID: {product_id}, Quantity: 1",
                "userId": user_id
            }
            logger.info(f"Adding product {product_id} to cart for user {user_id}")
            response = self.session.post(url, json=payload, timeout=10)

            if response.status_code == 201:
                cart = response.json()
                logger.info("Cart created successfully")
                return cart
            else:
                logger.error(f"Failed to add to cart: {response.status_code}")
                return None
        except requests.RequestException as e:
            logger.error(f"Add to cart request failed: {e}")
            return None

    def get_carts(self) -> List[Dict[str, Any]]:
        """Get list of posts (simulating carts)."""
        try:
            url = f"{self.base_url}/posts"
            logger.info("Fetching carts (posts)")
            response = self.session.get(url, timeout=10)

            if response.status_code == 200:
                carts = response.json()
                logger.info(f"Retrieved {len(carts)} carts")
                return carts
            else:
                logger.error(f"Failed to get carts: {response.status_code}")
                return []
        except requests.RequestException as e:
            logger.error(f"Get carts request failed: {e}")
            return []