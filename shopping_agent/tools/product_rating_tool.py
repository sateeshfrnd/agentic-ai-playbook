import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from shopping_agent.db.queries import get_product_rating


get_product_rating_tool_schema = {
    "name": "get_product_rating",
    "description": "Get average rating and number of reviews for a product",
    "parameters": {
        "type": "object",
        "properties": {
            "product_id": {
                "type": "integer",
                "description": "ID of the product"
            }
        },
        "required": ["product_id"]
    }
}

def get_product_rating_tool(product_id: int):
    """
    Get average rating and total reviews for a product
    """    
    return get_product_rating(product_id=product_id)


if __name__ == "__main__":
    response = get_product_rating_tool(product_id=1)
    print(response)