import mysql.connector
from datetime import datetime

class Database:
    
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="12345678"
            )
            cursor = conn.cursor()

            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS pos_db")
            cursor.execute("USE pos_db")

            # Create table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(225)
                )
            """)

            conn.commit()
            conn.close()
            print("Database CONNECTED  successfully!")

        except mysql.connector.Error as err:
            print(f" Error: {err}")


