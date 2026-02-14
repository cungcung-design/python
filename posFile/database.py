import mysql.connector
from mysql.connector import Error

class Database:

    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = "12345678"  
        self.database = "pos_db"

    def setup_database(self):
        try:
          
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS pos_db")
            cursor.execute("USE pos_db")
            print("Database created and selected.")


        

        
            # Users
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(100) NOT NULL,
                    password VARCHAR(100) NOT NULL
                   
                )
            """)

            # Categories
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100)
                )
            """)

            # items
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    price DECIMAL(10,2),
                    barcode VARCHAR(225),
                    category_id INT,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                )
            """)

            # Staff
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS staff (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(225),
                    role VARCHAR(225)
                )
            """)
            #safe transtions
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS safe_transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    amount DECIMAL(10,2),
                    type VARCHAR(225),

                    date DATETIME,
                    staff_id int,
                    FOREIGN KEY (staff_Id) REFERENCES staff(id)
                )
            """)
            # Sales
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    items_id INT,
                    quantity INT,
                    total DECIMAL(10,2),
                    date DATETIME,
                    staff_id INT,
                    FOREIGN KEY (items_id) REFERENCES items(id),
                    FOREIGN KEY (staff_id) REFERENCES staff(id)
                )
            """)

            # Insert default admin
            cursor.execute("""
                INSERT IGNORE INTO users (username, password)
                VALUES ('admin', 'password')

            """)
            conn.commit()
            conn.close()
            print("Database setup complete")

        except mysql.connector.Error as e:
            raise Exception(f"Database setup failed: {e}")

    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor
        except mysql.connector.Error as e:
            raise Exception(f"Query execution failed: {e}")

    def fetch_all(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except mysql.connector.Error as e:
            raise Exception(f"Fetch failed: {e}")
    def close(self):
        if self.connection:
            self.connection.close()
Database().setup_database()

