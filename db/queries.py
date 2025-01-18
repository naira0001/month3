# queries.py

CREATE_TABLE_store = """
   CREATE TABLE IF NOT EXISTS store (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    size TEXT,
    price TEXT,
    photo TEXT,
    productid INTEGER
    )
"""

# Создаем таблицу products_details
CREATE_TABLE_products_details = '''
    CREATE TABLE IF NOT EXISTS products_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    productid INTEGER,
    category TEXT,
    infoproduct TEXT
)
'''

INSERT_store_query = """
    INSERT INTO store (name,size,price,photo,productid)
    VALUES (?,?,?,?,?)
"""
INSERT_products_details_query = """
    INSERT INTO products_details (productid,category,infoproduct)
    VALUES (?,?,?)
"""