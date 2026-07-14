import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from langchain.tools import tool

from shopping_agent.db.queries import (
    search_products,
    get_product_details,
    create_order,
    get_product_rating
)

# Search Tool
@tool
def search_products_tool(query: str = "", max_price: float = None, min_rating: float = None, category: str = None):
    """Search for products using filters like name, category, price, and rating"""
    return search_products(query, max_price, min_rating, category)


# Product Details Tool
@tool
def get_product_details_tool(product_id: int):
    """Get full product details including reviews"""
    return get_product_details(product_id)


# Rating Tool
@tool
def get_product_rating_tool(product_id: int):
    """Get average rating and total reviews for a product"""
    return get_product_rating(product_id)


# Order Tool
@tool
def create_order_tool(product_id: int, quantity: int):
    """Create an order for a product with given quantity"""
    return create_order(product_id, quantity)

