import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from shopping_agent.db.queries import create_order

def create_order_tool(product_id: int, quantity: int):
    """
    Create an order for a product with specified quantity
    """
    return create_order(product_id=product_id, quantity=quantity)


create_order_tool_schema = {
    "name": "create_order",
    "description": "Create an order for a product with given quantity",
    "parameters": {
        "type": "object",
        "properties": {
            "product_id": {
                "type": "integer",
                "description": "ID of the product"
            },
            "quantity": {
                "type": "integer",
                "description": "Number of items to order"
            }
        },
        "required": ["product_id", "quantity"]
    }
}

if __name__ == "__main__":
    response = create_order_tool(product_id=1, quantity=2)
    print(response)