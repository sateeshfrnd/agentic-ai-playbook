import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "retail_store.db")

import sqlite3

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop tables (for fresh start)
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS reviews")
    cursor.execute("DROP TABLE IF EXISTS orders")

    # PRODUCTS TABLE
    cursor.execute("""
    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        price REAL,
        stock INTEGER,
        brand TEXT
    )
    """)

    # REVIEWS TABLE
    cursor.execute("""
    CREATE TABLE reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        rating INTEGER,
        comment TEXT,
        user_name TEXT,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    """)

    # ORDERS TABLE
    cursor.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        quantity INTEGER,
        total_price REAL,
        status TEXT,
        FOREIGN KEY(product_id) REFERENCES products(id)
    )
    """)

    # -----------------------------
    # INSERT SAMPLE PRODUCTS
    # -----------------------------
    products = [
        ("iPhone 14", "Electronics", 999, 15, "Apple"),
        ("Galaxy S23", "Electronics", 899, 20, "Samsung"),
        ("MacBook Air", "Computers", 1200, 10, "Apple"),
        ("Dell XPS 13", "Computers", 1100, 8, "Dell"),
        ("Nike Running Shoes", "Fashion", 120, 50, "Nike"),
        ("Adidas Hoodie", "Fashion", 80, 40, "Adidas"),
        ("Coffee Maker", "Home Appliances", 60, 25, "Philips"),
        ("Air Fryer", "Home Appliances", 150, 18, "Instant")
    ]

    cursor.executemany("""
        INSERT INTO products (name, category, price, stock, brand)
        VALUES (?, ?, ?, ?, ?)
    """, products)

    # -----------------------------
    # INSERT SAMPLE REVIEWS
    # -----------------------------
    reviews = [
        (1, 5, "Amazing phone!", "Satish"),
        (1, 4, "Great but expensive", "Shiva"),
        (2, 4, "Very good Android", "Ramya"),
        (3, 5, "Perfect laptop for work", "Teja"),
        (4, 3, "Good but battery average", "Bhavishya"),
        (5, 5, "Super comfortable!", "Ruchit"),
        (6, 4, "Nice hoodie", "Kumar"),
        (7, 3, "Does the job", "Sai"),
        (8, 5, "Love cooking with this!", "SKumar")
    ]

    cursor.executemany("""
        INSERT INTO reviews (product_id, rating, comment, user_name)
        VALUES (?, ?, ?, ?)
    """, reviews)

    # -----------------------------
    # INSERT SAMPLE ORDERS
    # -----------------------------
    orders = [
        (1, 1, 999, "delivered"),
        (3, 1, 1200, "shipped"),
        (5, 2, 240, "processing"),
        (8, 1, 150, "delivered")
    ]

    cursor.executemany("""
        INSERT INTO orders (product_id, quantity, total_price, status)
        VALUES (?, ?, ?, ?)
    """, orders)

    conn.commit()
    conn.close()
    print("Database setup complete with sample data!")

if __name__ == "__main__":
    setup_database()