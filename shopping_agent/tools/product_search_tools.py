import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from shopping_agent.db.queries import search_products


search_products_tool_schema = {
    "name": "search_products",
    "description": "Search for products using filters like name, category, price, and rating",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search keyword (e.g., iPhone, shoes)"
            },
            "max_price": {
                "type": "number",
                "description": "Maximum price filter"
            },
            "min_rating": {
                "type": "number",
                "description": "Minimum rating (0-5)"
            },
            "category": {
                "type": "string",
                "description": "Product category"
            }
        }
    }
}

def search_products_tool(query: str = "", max_price: float = None, min_rating: float = None, category: str = None):
    """
    Search products with filters like name, price, rating, category
    """
    results = search_products(
        query = query, 
        max_price = max_price, 
        min_rating = min_rating, 
        category = category
    )
    
    return results


if __name__ == "__main__":
    response = search_products_tool(query="phone", max_price=1000)
    print(response)
