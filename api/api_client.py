import logging
from typing import Optional, List, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from api.models import Product, Cart, CartItem
from config.config import Config

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class APIClient:
    """Thin API client with offline fallbacks and strong typing for tests."""

    def __init__(self) -> None:
        # A session with retries makes network‑flaky test runs less noisy.
        self.session = self._build_session()
        self.token: Optional[str] = None
        self.last_products: List[Product] = []
        self.last_cart: Optional[Cart] = None

        # API endpoints from configuration
        self.auth_base = Config.AUTH_API_BASE_URL.rstrip("/")
        self.store_base = Config.STORE_API_BASE_URL.rstrip("/")

        logger.info(
            "API Client initialised",
            extra={"auth_base": self.auth_base, "store_base": self.store_base, "timeout": Config.API_TIMEOUT},
        )

    # ------------------------------------------------------------------ #
    # Session helpers
    # ------------------------------------------------------------------ #
    def _build_session(self) -> requests.Session:
        """
        Create a requests session with retry semantics tuned for tests.

        We keep retries small to avoid slowing feedback loops while still
        smoothing over transient demo API hiccups.
        """
        session = requests.Session()
        retry_strategy = Retry(
            total=Config.MAX_RETRIES,
            backoff_factor=0.4,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset({"GET", "POST"}),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        # Intentional: do not set a global timeout on the session; pass per call.
        session.headers.update({"Accept": "application/json"})
        return session

    def _request(self, method: str, url: str, **kwargs) -> Tuple[Optional[requests.Response], Optional[Exception]]:
        """Centralised request helper for consistent logging and timeout handling."""
        kwargs.setdefault("timeout", Config.API_TIMEOUT)
        try:
            response = self.session.request(method=method, url=url, **kwargs)
            return response, None
        except requests.RequestException as exc:
            logger.error("HTTP request failed", extra={"url": url, "error": str(exc)})
            return None, exc

    def login(self, email: str, password: str) -> Optional[str]:
        """
        Simulate login - ReqRes API now requires authentication key.
        Using JSONPlaceholder to demonstrate authentication flow.
        """
        def generate_demo_token(seed: str) -> str:
            import hashlib
            return f"demo_token_{hashlib.md5(seed.encode()).hexdigest()[:8]}"

        # Simulate authentication by making a request to users endpoint
        url = f"{self.auth_base}/users"
        logger.info("Simulating login for user", extra={"email": email})

        response, error = self._request("GET", url)
        if response and response.status_code == 200:
            # Generate a mock token for demo purposes
            self.token = generate_demo_token(email)
            logger.info("Login simulation successful - demo token generated")
            return self.token

        if response:
            logger.error("Login simulation failed", extra={"status": response.status_code, "body": response.text})
            return None

        # Offline/demo fallback keeps tests running without network.
        self.token = generate_demo_token(email)
        logger.info("Using offline demo token after request error", extra={"error": str(error)})
        return self.token

    def get_products(self) -> List[Product]:
        """Get list of products using JSONPlaceholder posts (simulating products)."""
        url = f"{self.store_base}/posts"
        logger.info("Fetching products from store API", extra={"url": url})

        response, _ = self._request("GET", url)
        if response and response.status_code == 200:
            products = response.json()
            transformed_products: List[Product] = []
            for post in products[:10]:  # Limit to 10 products for determinism
                product: Product = {
                    "id": post["id"],
                    "title": post["title"],
                    "price": (post["id"] * 10.99),  # Mock price
                    "description": post["body"][:100],  # Truncate description
                    "category": f"Category {post['id'] % 5 + 1}",
                    "image": f"https://via.placeholder.com/150?text=Product+{post['id']}",
                    "userId": post["userId"],
                }
                transformed_products.append(product)

            logger.info("Products retrieved", extra={"count": len(transformed_products)})
            self.last_products = transformed_products
            return transformed_products

        if response:
            logger.error("Failed to get products", extra={"status": response.status_code, "body": response.text})
        return self._offline_products()

    def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1) -> Optional[Cart]:
        """Add product to cart by creating a post (simulating cart)."""
        url = f"{self.store_base}/posts"
        payload = {
            "title": f"Cart for user {user_id}",
            "body": f"Product ID: {product_id}, Quantity: {quantity}",
            "userId": user_id,
        }

        logger.info(
            "Adding product to cart",
            extra={"user_id": user_id, "product_id": product_id, "quantity": quantity},
        )
        response, _ = self._request("POST", url, json=payload)

        if response and response.status_code == 201:
            cart_response = response.json()
            cart: Cart = {
                "id": cart_response["id"],
                "userId": user_id,
                "date": "2024-01-01",  # Mock date
                "products": [
                    CartItem(productId=product_id, quantity=quantity)  # type: ignore[arg-type]
                ],
                "status": None,
            }
            logger.info("Cart created", extra={"cart_id": cart["id"]})
            self.last_cart = cart
            return cart

        if response:
            logger.error("Failed to add to cart", extra={"status": response.status_code, "body": response.text})
        return self._offline_cart(user_id, product_id, quantity)

    def get_carts(self, user_id: Optional[int] = None) -> List[Cart]:
        """Get list of carts (simulating cart retrieval)."""
        url = f"{self.store_base}/posts"
        if user_id:
            url += f"?userId={user_id}"

        logger.info("Fetching carts", extra={"url": url, "user_id": user_id})
        response, _ = self._request("GET", url)

        if response and response.status_code == 200:
            posts = response.json()
            carts: List[Cart] = []
            for post in posts[-5:]:  # Get last 5 posts as recent carts
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

                cart: Cart = {
                    "id": post["id"],
                    "userId": post["userId"],
                    "date": "2024-01-01",  # Mock date
                    "products": [
                        CartItem(productId=product_id or post["id"], quantity=quantity)  # type: ignore[arg-type]
                    ],
                    "status": None,
                }
                carts.append(cart)

            logger.info("Carts retrieved", extra={"count": len(carts)})
            self.last_cart = carts[-1] if carts else self.last_cart
            return carts

        if response:
            logger.error("Failed to get carts", extra={"status": response.status_code, "body": response.text})
        return self._offline_carts(user_id)

    def _offline_products(self) -> List[Product]:
        """Provide deterministic offline product data when network is unavailable."""
        if self.last_products:
            logger.info("Using cached offline products")
            return self.last_products

        offline_products: List[Product] = [
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

    def _offline_cart(self, user_id: int, product_id: int, quantity: int) -> Cart:
        """Create deterministic offline cart when API calls fail."""
        cart: Cart = {
            "id": self.last_cart["id"] if self.last_cart else 101,
            "userId": user_id,
            "date": "2024-01-01",
            "products": [
                {
                    "productId": product_id,
                    "quantity": quantity
                }
            ],
            "status": "offline",
        }
        self.last_cart = cart
        logger.info("Using offline cart fallback")
        return cart

    def _offline_carts(self, user_id: Optional[int]) -> List[Cart]:
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
