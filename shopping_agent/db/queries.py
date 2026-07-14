import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "retail_store.db")

# -----------------------------------
# SEARCH PRODUCTS
# -----------------------------------
def search_products(query="", max_price=None, min_rating=None, category=None, brand=None):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Base query with LEFT JOIN for ratings
        sql = """
        SELECT 
            p.id,
            p.name,
            p.category,
            p.price,
            p.brand,
            IFNULL(AVG(r.rating), 0) as avg_rating
        FROM products p
        LEFT JOIN reviews r ON p.id = r.product_id
        WHERE 1=1
        """
        params = []

        if query:
            sql += " AND name LIKE ?"
            params.append(f"%{query}%")    

        if max_price:
            sql += " AND price <= ?"
            params.append(max_price)
            
        if category:
            sql += " AND category = ?"
            params.append(category)

        if brand:
            sql += " AND brand = ?"
            params.append(brand)

        # Group by for aggregation
        sql += " GROUP BY p.id"

        if min_rating:
            sql += " HAVING avg_rating >= ?"
            params.append(min_rating)

        # print("Executing SQL:", sql)
        # print("With parameters:", params)
        cursor.execute(sql, params)
        results = cursor.fetchall()
        conn.close()

        return {
            "success": True,
            "data": [
                {
                    "id": r[0],
                    "name": r[1],
                    "category": r[2],
                    "price": r[3],
                    "brand": r[4],
                    "rating": round(r[5], 2)
                }
                for r in results
            ],
            "error": None
        }
    except Exception as e:
        print("Error during search_products:", str(e))
        return {
            "success": False,
            "data": [],
            "error": str(e)
        }

# -----------------------------------
# GET PRODUCT DETAILS
# -----------------------------------
def get_product_details(product_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        sql = """
        SELECT id, name, category, price, brand, stock
        FROM products
        WHERE id = ?
        """

        cursor.execute(sql, (product_id,))
        product = cursor.fetchone()

        if not product:
            conn.close()
            return {
                    "success": False,
                    "data": None,
                    "error": f"Product with id {product_id} not found"
                }

        cursor.execute("SELECT rating, comment, user_name FROM reviews WHERE product_id = ?", (product_id,))
        reviews = cursor.fetchall()
        # print(f'reviews for product {product_id}:', reviews)

        result = {
                "id": product[0],
                "name": product[1],
                "category": product[2],
                "price": product[3],
                "brand": product[4],   # ✅ fixed
                "stock": product[5],   # ✅ fixed
                "reviews": [
                    {
                        "rating": r[0],
                        "comment": r[1],
                        "user_name": r[2]
                    }
                    for r in reviews
                ]
            }

        conn.close()
        return {
                "success": True,
                "data": result,
                "error": None
            }
    except Exception as e:
        print("Error during get_product_details:", str(e))
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }


# -----------------------------------
# GET PRODUCT RATING
# -----------------------------------
def get_product_rating(product_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        sql = """
        SELECT 
            AVG(rating), COUNT(*)
        FROM reviews
        WHERE product_id = ?
        """

        cursor.execute(sql, (product_id,))
        result = cursor.fetchone()

        conn.close()

        if result and result[0] is not None:
            return {
                "success": True,
                "data": {
                "product_id": product_id,
                "avg_rating": round(result[0], 2),
                "total_reviews": result[1]
                },
                "error": None
            }
        else:
            return {
                "success": True,
                "data": {
                    "product_id": product_id,
                    "avg_rating": 0,
                    "total_reviews": 0
                },
                "error": None
            }   
               
    except Exception as e:
        print("Error during get_product_rating:", str(e))
        return {
            "success": False,
            "data": None,
            "error": str(e)
        }
    


def create_order(product_id, quantity):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check product exists
    cursor.execute("""
        SELECT name, price, stock 
        FROM products 
        WHERE id = ?
    """, (product_id,))
    
    product = cursor.fetchone()

    if not product:
        conn.close()
        return {"error": "Product not found"}

    name, price, stock = product

    # Check stock 
    if stock < quantity:
        conn.close()
        return {"error": "Not enough stock"}

    # Calculate total price
    total_price = price * quantity

    # Insert order
    cursor.execute("""
        INSERT INTO orders (product_id, quantity, total_price, status)
        VALUES (?, ?, ?, ?)
    """, (product_id, quantity, total_price, "processing"))

    # Update stock
    cursor.execute(
        "UPDATE products SET stock = stock - ? WHERE id = ?",
        (quantity, product_id)
    )

    conn.commit()
    conn.close()

    return {
        "success": True,
        "data": {
            "message": "Order placed successfully",
            "product": name,
            "quantity": quantity,
            "total_price": total_price,
            "status": "processing"
        },
        "error": None
    }
   
       
if __name__ == "__main__":
    # Test cases
    print("\n =====Test 1: Search 'iphone' =====")
    results = search_products(query="iphone")
    print("results", results)

    print("\n =====Test 2: Max price 1000 =====")
    results = search_products(max_price=1000)
    print("results", results)

    print("\n =====Test 3: Category = Electronics =====")
    results = search_products(category="Electronics")
    print("results", results)

    print("\n =====Test 4: Min rating 4 =====")
    results = search_products(min_rating=4)
    print("results", results)

    print("\n =====Test 5: Combined filters =====")
    results = search_products(query="apple", max_price=1200, category="Computers", min_rating=4)
    print("results", results)

    print("\n =====Test 6: No match case =====")
    results = search_products(query="xyz123")
    print("results", results)

    print("\n ==== Test 7: Product Rating (ID=1)")
    rating = get_product_rating(1)
    print(rating)

    print("\n Product Details (ID=1)")
    details = get_product_details(1)
    print(details)

    # print("\n Create Order (Product ID=1, Qty=2)")
    # order = create_order(1, 2)
    # print(order)

    # print("\n Create Order (Product ID=999, Qty=1)")
    # order = create_order(999, 1)
    # print(order)

    # print("\n Create Order (Product ID=1, Qty=100)")
    # order = create_order(1, 100)    
    # print(order)