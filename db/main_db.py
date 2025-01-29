# main_db.py
import sqlite3
from db import queries

db = sqlite3.connect('db/store.sqlite3')
cursor = db.cursor()

async def create_db():
    if db:
        print('База данных подключена')
        # Создаем таблицы, если их еще нет
    cursor.execute(queries.CREATE_TABLE_store)
    cursor.execute(queries.CREATE_TABLE_products_details)
    cursor.execute(queries.CREATE_TABLE_collections)


async def sql_insert_store(name, size, price, photo, productid):
    cursor.execute(queries.INSERT_store_query, (
        name, size, price, photo, productid
    ))
    db.commit()

async def sql_insert_products_details(productid, category, infoproduct):
    cursor.execute(queries.INSERT_products_details_query,(
        productid, category, infoproduct
     ))
    db.commit()

async def sql_insert_collections(collection, productid):
    cursor.execute(queries.INSERT_collections_query,(
        collection, productid
     ))
    db.commit()

# CRUD - 1
# ==================================================================
def get_db_connection():
    conn = sqlite3.connect('db/store.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_products():
    conn = get_db_connection()
    products = conn.execute("""
    SELECT * FROM store s
    INNER JOIN  products_details pd on s.productid = pd.productid
    INNER JOIN  collections cl on cl.productid = s.productid 
    """).fetchall()
    conn.close()
    return products

def delete_product(productid):
    conn = get_db_connection()
    conn.execute('DELETE FROM store WHERE productid = ?', (productid,))
    conn.execute('DELETE FROM products_details WHERE productid = ?', (productid,))
    conn.execute('DELETE FROM collections WHERE productid = ?', (productid,))
    conn.commit()
    conn.close()

# CRUD - update
# ==================================================================
def update_product_field(productid, field_name, new_value):
    conn = get_db_connection()
    store_table = ['name', 'size', 'price', 'photo']
    products_details_table = ['category', 'infoproduct']
    collections_table = ['collection']
    try:
        if field_name in store_table:
            query = f"UPDATE store SET {field_name} = ? WHERE productid = ?"
        elif field_name in products_details_table:
            query = f"UPDATE products_details SET {field_name} = ? WHERE productid = ?"
        elif field_name in collections_table:
            query = f"UPDATE collections SET {field_name} = ? WHERE productid = ?"
        else:
            raise ValueError(f'Нет такого поля как {field_name}')
        conn.execute(query, (new_value, productid))
        conn.commit()
    except sqlite3.OperationalError as e:
        print(f'Ошибка - {e}')
    finally:
        conn.close()