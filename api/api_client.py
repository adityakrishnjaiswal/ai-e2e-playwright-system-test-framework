import requests
import logging
from typing import Dict, Any, Optional, List
from config.config import Config

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class APIClient:
    """API client for e-commerce system testing with authentication, products, and cart operations."""

    def __init__(self):
        self.session = requests.Session()
        self.token: Optional[str] = None

        # API endpoints from configuration
        self.auth_base = Config.AUTH_API_BASE_URL
        self.store_base = Config.STORE_API_BASE_URL

        # Configure session with timeout
        self.session.timeout = Config.API_TIMEOUT

        logger.info(f"API Client initialized with auth_base: {self.auth_base}, store_base: {self.store_base}")

    def login(self, email: str, password: str) -> Optional[str]:
        """
        Simulate login - ReqRes API now requires authentication key.
        Using JSONPlaceholder to demonstrate authentication flow.
        """
        try:
            # Simulate authentication by making a request to users endpoint
            # In real scenario, this would be actual authentication
            url = f"{self.auth_base}/users"
            logger.info(f"Simulating login for user: {email}")

            response = self.session.get(url, timeout=Config.API_TIMEOUT)

            if response.status_code == 200:
                # Generate a mock token for demo purposes
                # In production, this would come from actual authentication
                import hashlib
                self.token = f"demo_token_{hashlib.md5(email.encode()).hexdigest()[:8]}"
                logger.info("Login simulation successful - demo token generated")
                return self.token
            else:
                logger.error(f"Login simulation failed: {response.status_code}")
                return None

        except requests.RequestException as e:
            logger.error(f"Login simulation request failed: {e}")
            return None

    def get_products(self) -> List[Dict[str, Any]]:
        """Get list of products using JSONPlaceholder posts (simulating products)."""
        try:
            url = f"{self.store_base}/posts"
            logger.info("Fetching products from store API")
            response = self.session.get(url, timeout=Config.API_TIMEOUT)

            if response.status_code == 200:
                products = response.json()
                # Transform posts to product-like structure for demo
                transformed_products = []
                for post in products[:10]:  # Limit to 10 products
                    product = {
                        "id": post["id"],
                        "title": post["title"],
                        "price": (post["id"] * 10.99),  # Mock price
                        "description": post["body"][:100],  # Truncate description
                        "category": f"Category {post['id'] % 5 + 1}",
                        "image": f"https://via.placeholder.com/150?text=Product+{post['id']}",
                        "userId": post["userId"]
                    }
                    transformed_products.append(product)

                logger.info(f"Retrieved {len(transformed_products)} products successfully")
                return transformed_products
            else:
                logger.error(f"Failed to get products: {response.status_code} - {response.text}")
                return []

        except requests.RequestException as e:
            logger.error(f"Get products request failed: {e}")
            return []

    def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1) -> Optional[Dict[str, Any]]:
        """Add product to cart by creating a post (simulating cart)."""
        try:
            url = f"{self.store_base}/posts"
            payload = {
                "title": f"Cart for user {user_id}",
                "body": f"Product ID: {product_id}, Quantity: {quantity}",
                "userId": user_id
            }

            logger.info(f"Adding product {product_id} (quantity: {quantity}) to cart for user {user_id}")
            response = self.session.post(url, json=payload, timeout=Config.API_TIMEOUT)

            if response.status_code == 201:
                cart_response = response.json()
                # Transform to cart-like structure
                cart = {
                    "id": cart_response["id"],
                    "userId": user_id,
                    "date": "2024-01-01",  # Mock date
                    "products": [
                        {
                            "productId": product_id,
                            "quantity": quantity
                        }
                    ]
                }
                logger.info(f"Cart created successfully with ID: {cart['id']}")
                return cart
            else:
                logger.error(f"Failed to add to cart: {response.status_code} - {response.text}")
                return None

        except requests.RequestException as e:
            logger.error(f"Add to cart request failed: {e}")
            return None

    def get_carts(self, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get list of carts (simulating cart retrieval)."""
        try:
            url = f"{self.store_base}/posts"
            if user_id:
                url += f"?userId={user_id}"

            logger.info(f"Fetching carts from store API{' for user ' + str(user_id) if user_id else ''}")
            response = self.session.get(url, timeout=Config.API_TIMEOUT)

            if response.status_code == 200:
                posts = response.json()
                # Transform posts to cart-like structure
                carts = []
                for post in posts[-5:]:  # Get last 5 posts as recent carts
                    # Extract product info from post body
                    body = post.get("body", "")
                    product_id = None
                    quantity = 1

                    if "Product ID:" in body:
                        try:
                            product_part = body.split("Product ID:")[1].split(",")[0].strip()
                            product_id = int(product_part)
                            if "Quantity:" in body:
                                quantity_part = body.split("Quantity:")[1].strip()
                                quantity = int(quantity_part)
                        except (ValueError, IndexError):
                            product_id = post["id"]  # Fallback

                    cart = {
                        "id": post["id"],
                        "userId": post["userId"],
                        "date": "2024-01-01",  # Mock date
                        "products": [
                            {
                                "productId": product_id or post["id"],
                                "quantity": quantity
                            }
                        ]
                    }
                    carts.append(cart)

                logger.info(f"Retrieved {len(carts)} carts successfully")
                return carts
            else:
                logger.error(f"Failed to get carts: {response.status_code} - {response.text}")
                return []

        except requests.RequestException as e:
            logger.error(f"Get carts request failed: {e}")
            return []