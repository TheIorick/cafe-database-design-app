import random

from flask import Flask, render_template
import psycopg2
from constant_db_tables import ConstantDBTables

app = Flask(__name__)


def fill_tables_with_dummy_data():
    conn = get_db_connection()
    if not conn:
        print("Ошибка подключения к базе данных")
        return
    try:
        with conn.cursor() as cursor:
            # Добавляем липовые данные в таблицу products
            # for i in range(10):  # Пример: добавляем 10 записей
            #     cursor.execute(
            #         f"INSERT INTO {ConstantDBTables.PRODUCTS_TABLE} ({ConstantDBTables.NAME_PRODUCTS}, {ConstantDBTables.QUANTITY_PRODUCTS}) VALUES (%s, %s)",
            #         (f'Product_{i}', random.randint(1, 100))  # Имя продукта и случайное количество на складе
            #     )

            # Добавляем липовые данные в таблицу purchase_order

            # Фиксируем изменения в базе данных
            conn.commit()
            cursor.execute(f"SELECT {ConstantDBTables.ID_PRODUCTS} FROM {ConstantDBTables.PRODUCTS_TABLE}")
            product_ids = cursor.fetchall()

            # Insert data into ORDER_COMPOSITION_TABLE
            for product_id in product_ids:
                cursor.execute(
                    f"INSERT INTO {ConstantDBTables.ORDER_COMPOSITION_TABLE} ({ConstantDBTables.ID_PRODUCTS}, {ConstantDBTables.QUANTITY_ITEM}) VALUES (%s, %s)",
                    (product_id[0], random.randint(1, 100))  # Random quantity between 1 and 100
                )
            conn.commit()
        print("Data added to ORDER_COMPOSITION_TABLE")
        print("Данные добавлены")
    except Exception as e:
        print("Ошибка при добавлении данных:", e)
    finally:
        if conn:
            conn.close()


# Подключение к базе данных
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname='vsu_3_curs_create_db_cafe',
            user='postgres',
            password='123',
            host='localhost',
            port='5432'
        )
        return conn
    except Exception as e:
        print("Can't establish connection to database:", e)
        return None


def fill_purchase_order_table():
    conn = get_db_connection()
    if not conn:
        return "Ошибка подключения к базе данных"
    try:
        with conn.cursor() as cursor:
            # Получение данных из других таблиц
            cursor.execute("SELECT id_suppliers FROM suppliers")
            suppliers = cursor.fetchall()

            cursor.execute("SELECT id_composition, quantity_item FROM order_composition")
            compositions = cursor.fetchall()
            print(random.choice(compositions)[0])
            # Генерация и вставка данных в PURCHASE_ORDER_TABLE
            for _ in range(100):  # Генерируем 100 записей
                id_supplier = random.choice(suppliers)[0] if suppliers else None
                id_composition = random.choice(compositions)[0] if compositions else None
                cost_delivery_value = random.randint(100, 1000)
                payment_method = random.choice(['Credit Card', 'Cash', 'Bank Transfer'])

                cursor.execute(
                    f"INSERT INTO {ConstantDBTables.PURCHASE_ORDER_TABLE} "
                    f"({ConstantDBTables.ID_SUPPLIERS}, {ConstantDBTables.ID_COMPOSITION}, "
                    f"{ConstantDBTables.COST_DELIVERY_VALUE}, {ConstantDBTables.PAYMENT_METHOD}) "
                    f"VALUES (%s, %s, %s, %s)",
                    (id_supplier, id_composition, cost_delivery_value, payment_method)
                )
            conn.commit()
            print("Данные успешно добавлены в PURCHASE_ORDER_TABLE")
    except Exception as e:
        print("Ошибка при добавлении данных:", e)
    finally:
        if conn:
            conn.close()


def get_suppliers():
    suppliers = []
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                f"SELECT {ConstantDBTables.ID_SUPPLIERS}, {ConstantDBTables.COMPANY_NAME}, {ConstantDBTables.PRICE_SERVICES} FROM {ConstantDBTables.SUPPLIERS_TABLE}")
            suppliers = cursor.fetchall()
    except Exception as e:
        print("Error when fetching data:", e)
    finally:
        if conn:
            conn.close()
    return suppliers


@app.route('/')
def index():
    suppliers = get_suppliers()
    all_data()
    return render_template('index.html', suppliers=suppliers)


@app.route('/purchase_orders')
def purchase_orders():
    conn = get_db_connection()
    if not conn:
        return "Ошибка подключения к базе данных"

    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {ConstantDBTables.PURCHASE_ORDER_TABLE}")
            purchase_orders = cursor.fetchall()
    except Exception as e:
        return f"Ошибка при получении данных: {e}"
    finally:
        if conn:
            conn.close()

    return render_template('purchase_orders.html', purchase_orders=purchase_orders)


@app.route('/products')
def products():
    conn = get_db_connection()
    if not conn:
        return "Ошибка подключения к базе данных"

    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {ConstantDBTables.PRODUCTS_TABLE}")
            products = cursor.fetchall()
    except Exception as e:
        return f"Ошибка при получении данных: {e}"
    finally:
        if conn:
            conn.close()

    return render_template('products.html', products=products)


@app.route('/all_data')
def all_data():
    conn = get_db_connection()
    if not conn:
        return "Ошибка подключения к базе данных"

    try:
        with conn.cursor() as cursor:
            # Получение данных из таблицы поставщиков
            cursor.execute(f"SELECT * FROM {ConstantDBTables.SUPPLIERS_TABLE}")
            suppliers = cursor.fetchall()

            # Получение данных из таблицы заказов на покупку
            cursor.execute(f"SELECT * FROM {ConstantDBTables.PURCHASE_ORDER_TABLE}")
            purchase_orders = cursor.fetchall()

            # Получение данных из таблицы продуктов
            cursor.execute(f"SELECT * FROM {ConstantDBTables.PRODUCTS_TABLE}")
            products = cursor.fetchall()
    except Exception as e:
        return f"Ошибка при получении данных: {e}"
    finally:
        if conn:
            conn.close()

    return render_template('all_data.html', suppliers=suppliers, purchase_orders=purchase_orders, products=products)


if __name__ == '__main__':
    # fill_tables_with_dummy_data()
    fill_purchase_order_table()
    app.run(debug=True)
