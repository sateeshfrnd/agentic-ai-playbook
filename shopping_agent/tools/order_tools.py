from langchain.tools import tool

import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from shopping_agent.db.queries import create_order

@tool
def checkout(product_id: int, quantity: int):
    """
    Place an order for a product
    """
    return create_order(product_id, quantity)