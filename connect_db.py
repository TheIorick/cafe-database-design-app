from flask import *

from constant_db_tables import ConstantDBTables
from data_manager import DataManager
from database_connection import  DatabaseConnection

app = Flask(__name__)

db_connection = DatabaseConnection(
    dbname='vsu_3_curs_create_db_cafe',
    user='postgres',
    password='123',
    host='localhost',
    port='5432'
)

data_manager = DataManager(db_connection)

@app.route('/')
def index():
    conn = db_connection.connect()
    if not conn:
        return "Ошибка подключения к базе данных"

    try:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {ConstantDBTables.SUPPLIERS_TABLE}")
            suppliers = cursor.fetchall()

            cursor.execute(f"SELECT * FROM {ConstantDBTables.PURCHASE_ORDER_TABLE}")
            purchase_orders = cursor.fetchall()

            cursor.execute(f"SELECT * FROM {ConstantDBTables.PRODUCTS_TABLE}")
            products = cursor.fetchall()
    except Exception as e:
        return f"Ошибка при получении данных: {e}"
    finally:
        db_connection.close()

    return render_template('index.html', suppliers=suppliers, purchase_orders=purchase_orders, products=products)

if __name__ == '__main__':
    app.run(debug=True)
