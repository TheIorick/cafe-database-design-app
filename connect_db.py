import psycopg2
from constant_db_tables import ConstantDBTables
import random

try:
    conn = psycopg2.connect(dbname='vsu_3_curs_create_db_cafe', user='postgres', password='123', host='localhost', port='5432')
    print("Connect")
except Exception as e:
    print("Can't establish connection to database:", e)

try:
    with conn.cursor() as cursor:
        # Вставляем несколько одинаковых значений
        for i in range(1000):  # Пример: добавляем 5 одинаковых записей
            cursor.execute(
                f"INSERT INTO {ConstantDBTables.SUPPLIERS_TABLE} ({ConstantDBTables.PRICE_SERVICES}, {ConstantDBTables.COMPANY_NAME}) VALUES (%s, %s)",
                (random.randint(1000, 10000), 'FERMA' + str(i))
            )
    conn.commit()
    print("Данные добавлены")
except Exception as e:
    print("Ошибка при добавлении данных:", e)
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
