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


async def sql_insert_store(name, size, price, photo, productid):
    cursor.execute(queries.INSERT_store_query, (
        name, size, price, photo, productid
    ))
    db.commit()

async def sql_insert_product_details(productid, category, infoproduct):
    cursor.execute(queries.INSERT_products_details_query,(
        productid, category, infoproduct
     ))
    db.commit()
