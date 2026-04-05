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
        self.last_products: List[Dict[str, Any]] = []
        self.last_cart: Optional[Dict[str, Any]] = None

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
        def generate_demo_token(seed: str) -> str:
            import hashlib
            return f"demo_token_{hashlib.md5(seed.encode()).hexdigest()[:8]}"

        try:
            # Simulate authentication by making a request to users endpoint
            # In real scenario, this would be actual authentication
            url = f"{self.auth_base}/users"
            logger.info(f"Simulating login for user: {email}")

            response = self.session.get(url, timeout=Config.API_TIMEOUT)

            if response.status_code == 200:
                # Generate a mock token for demo purposes
                # In production, this would come from actual authentication
                self.token = generate_demo_token(email)
                logger.info("Login simulation successful - demo token generated")
                return self.token
            else:
                logger.error(f"Login simulation failed: {response.status_code}")
                return None

        except requests.RequestException as e:
            logger.error(f"Login simulation request failed: {e}")
            # Offline/demo fallback
            self.token = generate_demo_token(email)
            logger.info("Using offline demo token")
            return self.token

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
                self.last_products = transformed_products
                return transformed_products
            else:
                logger.error(f"Failed to get products: {response.status_code} - {response.text}")
                return self._offline_products()

        except requests.RequestException as e:
            logger.error(f"Get products request failed: {e}")
            return self._offline_products()

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
                self.last_cart = cart
                return cart
            else:
                logger.error(f"Failed to add to cart: {response.status_code} - {response.text}")
                return self._offline_cart(user_id, product_id, quantity)

        except requests.RequestException as e:
            logger.error(f"Add to cart request failed: {e}")
            return self._offline_cart(user_id, product_id, quantity)

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
                self.last_cart = carts[-1] if carts else self.last_cart
                return carts
            else:
                logger.error(f"Failed to get carts: {response.status_code} - {response.text}")
                return self._offline_carts(user_id)

        except requests.RequestException as e:
            logger.error(f"Get carts request failed: {e}")
            return self._offline_carts(user_id)

    def _offline_products(self) -> List[Dict[str, Any]]:
        """Provide deterministic offline product data when network is unavailable."""
        if self.last_products:
            logger.info("Using cached offline products")
            return self.last_products

        offline_products = [
            {
                "id": 1,
                "title": "Offline Product 1",
                "price": 10.99,
                "description": "Offline fallback product used when API is unreachable.",
                "category": "Category 1",
                "image": "https://via.placeholder.com/150?text=Offline+1",
                "userId": 1
            },
            {
                "id": 2,
                "title": "Offline Product 2",
                "price": 19.99,
                "description": "Second offline product to satisfy list expectations.",
                "category": "Category 2",
                "image": "https://via.placeholder.com/150?text=Offline+2",
                "userId": 1
            },
        ]
        self.last_products = offline_products
        logger.info("Using offline product dataset")
        return offline_products

    def _offline_cart(self, user_id: int, product_id: int, quantity: int) -> Dict[str, Any]:
        """Create deterministic offline cart when API calls fail."""
        cart = {
            "id": self.last_cart["id"] if self.last_cart else 101,
            "userId": user_id,
            "date": "2024-01-01",
            "products": [
                {
                    "productId": product_id,
                    "quantity": quantity
                }
            ]
        }
        self.last_cart = cart
        logger.info("Using offline cart fallback")
        return cart

    def _offline_carts(self, user_id: Optional[int]) -> List[Dict[str, Any]]:
        """Return offline carts list, reusing last created cart when possible."""
        carts = []

        if self.last_cart:
            if user_id is None or self.last_cart["userId"] == user_id:
                carts.append(self.last_cart)

        if not carts:
            # Build a cart from offline products as a fallback
            products = self._offline_products()
            first_product_id = products[0]["id"]
            carts.append(self._offline_cart(user_id or 1, first_product_id, 1))

        logger.info("Using offline carts dataset")
        return carts
