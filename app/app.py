import mysql.connector
import time
from datetime import datetime

# Подключение к базе данных
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootpass",
    database="test_db",
    port=3310
)
cursor = conn.cursor()

try:
    while True:
        # Подготовка данных для вставки 10 записей
        data_to_insert = [
            ("test_name_" + str(i), datetime.now()) for i in range(10)
        ]

        # Выполнение множественной вставки
        cursor.executemany(
            "INSERT INTO test_table (name, timestamp) VALUES (%s, %s)",
            data_to_insert
        )

        # Подтверждение транзакции
        conn.commit()
        print("10 records inserted")

        # Пауза 5 секунд перед следующей вставкой
        time.sleep(5)
        break

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Закрытие соединения
    conn.close()