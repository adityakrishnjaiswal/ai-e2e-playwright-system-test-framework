"""
Typed structures used by the test automation framework.

These `TypedDict` definitions keep responses flexible (still plain dicts for
Playwright/requests consumers) while giving IDEs and static checkers enough
shape to catch mistakes early—similar to the rigor a senior SDET would expect.
"""

from typing import TypedDict, List, Optional


class Product(TypedDict):
    id: int
    title: str
    price: float
    description: str
    category: str
    image: str
    userId: int


class CartItem(TypedDict):
    productId: int
    quantity: int


class Cart(TypedDict):
    id: int
    userId: int
    date: str
    products: List[CartItem]
    # Store API responses are inconsistent; keep optional fields explicit.
    # `Optional` keeps mypy/pyright quiet without altering runtime shape.
    status: Optional[str]
