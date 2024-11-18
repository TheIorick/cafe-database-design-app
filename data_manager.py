from random import random

from constant_db_tables import ConstantDBTables


class DataManager:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def fill_purchase_order_table(self):
        conn = self.db_connection.connect()
        if not conn:
            return "Ошибка подключения к базе данных"
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id_suppliers FROM suppliers")
                suppliers = cursor.fetchall()

                cursor.execute("SELECT id_composition, quantity_item FROM order_composition")
                compositions = cursor.fetchall()

                for _ in range(100):
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
            self.db_connection.close()

    def get_suppliers(self):
        suppliers = []
        try:
            conn = self.db_connection.connect()
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT {ConstantDBTables.ID_SUPPLIERS}, {ConstantDBTables.COMPANY_NAME}, {ConstantDBTables.PRICE_SERVICES} FROM {ConstantDBTables.SUPPLIERS_TABLE}")
                suppliers = cursor.fetchall()
        except Exception as e:
            print("Ошибка при получении данных:", e)
        finally:
            self.db_connection.close()
        return suppliers
