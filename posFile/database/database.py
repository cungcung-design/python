import bcrypt
import mysql.connector
from mysql.connector import Error

from config.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def get_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )

        if connection.is_connected():
            print("MySQL connected successfully.")
            return connection

    except Error as e:
        print(f"MySQL connection failed: {e}")

    return None


class Database:
    def __init__(self):
        self.host = DB_HOST
        self.port = DB_PORT
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.database = DB_NAME
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )
        except mysql.connector.Error:
            try:
                conn = mysql.connector.connect(
                    host=self.host, port=self.port, user=self.user, password=self.password
                )
                cursor = conn.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS pos_db")
                conn.close()
                self.connection = mysql.connector.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                )
            except mysql.connector.Error as e:
                print(f"Could not connect to database: {e}")
                self.connection = None

    def setup_database(self):
        try:
            conn = mysql.connector.connect(
                host=self.host, port=self.port, user=self.user, password=self.password
            )
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS pos_db")
            cursor.execute("USE pos_db")
            print("Database created and selected.")

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(100) NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    role VARCHAR(50) NOT NULL DEFAULT 'cashier',
                    staff_id INT NULL,
                    FOREIGN KEY (staff_id) REFERENCES staff(id)
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100)
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100),
                    price DECIMAL(10,2),
                    barcode VARCHAR(225),
                    category_id INT,
                    stock INT NOT NULL DEFAULT 0,
                    FOREIGN KEY (category_id) REFERENCES categories(id)
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS staff (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(225),
                    role VARCHAR(225)
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS safe_transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    amount DECIMAL(10,2),
                    type VARCHAR(225),
                    date DATETIME,
                    staff_id INT,
                    FOREIGN KEY (staff_id) REFERENCES staff(id)
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sales (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    items_id INT,
                    quantity INT,
                    total DECIMAL(10,2),
                    date DATETIME,
                    user_id INT,
                    payment_method VARCHAR(30) DEFAULT 'Cash',
                    FOREIGN KEY (items_id) REFERENCES items(id),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS stock_transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    item_id INT NOT NULL,
                    quantity INT NOT NULL,
                    type VARCHAR(50) NOT NULL,
                    note VARCHAR(255),
                    date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    staff_id INT,
                    FOREIGN KEY (item_id) REFERENCES items(id),
                    FOREIGN KEY (staff_id) REFERENCES staff(id)
                )
            """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS cash_registers (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    staff_id INT NOT NULL,
                    opening_cash DECIMAL(10,2) NOT NULL DEFAULT 0,
                    closing_cash DECIMAL(10,2) DEFAULT NULL,
                    expected_cash DECIMAL(10,2) DEFAULT NULL,
                    difference DECIMAL(10,2) DEFAULT NULL,
                    opened_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    closed_at DATETIME DEFAULT NULL,
                    status VARCHAR(20) NOT NULL DEFAULT 'open',
                    FOREIGN KEY (staff_id) REFERENCES staff(id)
                )
            """
            )

            cursor.execute(
                """
                INSERT IGNORE INTO staff (name, role)
                VALUES ('Admin', 'admin')
            """
            )
            cursor.execute("SELECT id FROM staff WHERE name = 'Admin' LIMIT 1")
            staff_row = cursor.fetchone()
            staff_id = staff_row[0] if staff_row else None

            cursor.execute(
                """
                INSERT IGNORE INTO users (username, password, role, staff_id)
                VALUES (%s, %s, %s, %s)
            """,
                (
                    "admin",
                    bcrypt.hashpw(b"password", bcrypt.gensalt()).decode(),
                    "admin",
                    staff_id,
                ),
            )
            conn.commit()
            conn.close()

            # Migrate existing database schema
            self._migrate_schema()

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

    def begin_transaction(self):
        if self.connection:
            try:
                self.connection.start_transaction()
            except mysql.connector.errors.ProgrammingError as e:
                if "Transaction already in progress" not in str(e):
                    raise

    def commit(self):
        if self.connection:
            self.connection.commit()

    def rollback(self):
        if self.connection:
            self.connection.rollback()

    def close(self):
        if self.connection:
            self.connection.close()

    def _migrate_schema(self):
        try:
            cursor = self.connection.cursor()

            # Add staff_id to users if missing
            cursor.execute("SHOW COLUMNS FROM users LIKE 'staff_id'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE users ADD COLUMN staff_id INT NULL")
                cursor.execute(
                    "ALTER TABLE users ADD CONSTRAINT fk_users_staff FOREIGN KEY (staff_id) REFERENCES staff(id) ON DELETE SET NULL"
                )

            # Add stock to items if missing
            cursor.execute("SHOW COLUMNS FROM items LIKE 'stock'")
            if not cursor.fetchone():
                cursor.execute("ALTER TABLE items ADD COLUMN stock INT NOT NULL DEFAULT 0")

            # Add payment_method to sales if missing
            cursor.execute("SHOW COLUMNS FROM sales LIKE 'payment_method'")
            if not cursor.fetchone():
                cursor.execute(
                    "ALTER TABLE sales ADD COLUMN payment_method VARCHAR(30) DEFAULT 'Cash'"
                )

            # Create stock_transactions if missing
            cursor.execute("SHOW TABLES LIKE 'stock_transactions'")
            if not cursor.fetchone():
                cursor.execute(
                    """
                    CREATE TABLE stock_transactions (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        item_id INT NOT NULL,
                        quantity INT NOT NULL,
                        type VARCHAR(50) NOT NULL,
                        note VARCHAR(255),
                        date DATETIME DEFAULT CURRENT_TIMESTAMP,
                        staff_id INT,
                        FOREIGN KEY (item_id) REFERENCES items(id),
                        FOREIGN KEY (staff_id) REFERENCES staff(id)
                    )
                """
                )

            # Create cash_registers if missing
            cursor.execute("SHOW TABLES LIKE 'cash_registers'")
            if not cursor.fetchone():
                cursor.execute(
                    """
                    CREATE TABLE cash_registers (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        staff_id INT NOT NULL,
                        opening_cash DECIMAL(10,2) NOT NULL DEFAULT 0,
                        closing_cash DECIMAL(10,2) DEFAULT NULL,
                        expected_cash DECIMAL(10,2) DEFAULT NULL,
                        difference DECIMAL(10,2) DEFAULT NULL,
                        opened_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                        closed_at DATETIME DEFAULT NULL,
                        status VARCHAR(20) NOT NULL DEFAULT 'open',
                        FOREIGN KEY (staff_id) REFERENCES staff(id)
                    )
                """
                )

            # Migrate plaintext passwords to bcrypt
            cursor.execute("SELECT id, password FROM users")
            users = cursor.fetchall()
            for user_id, password in users:
                if password and not password.startswith("$2b$"):
                    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()
                    cursor.execute(
                        "UPDATE users SET password = %s WHERE id = %s",
                        (hashed, user_id),
                    )

            # Ensure admin user has a staff_id
            cursor.execute("SELECT id FROM users WHERE username = 'admin' LIMIT 1")
            admin_user = cursor.fetchone()
            if admin_user:
                cursor.execute("SELECT id FROM staff WHERE name = 'Admin' LIMIT 1")
                admin_staff = cursor.fetchone()
                if not admin_staff:
                    cursor.execute("INSERT INTO staff (name, role) VALUES ('Admin', 'admin')")
                    admin_staff_id = cursor.lastrowid
                else:
                    admin_staff_id = admin_staff[0]
                cursor.execute(
                    "UPDATE users SET staff_id = %s WHERE username = 'admin' AND staff_id IS NULL",
                    (admin_staff_id,),
                )

            self.connection.commit()
            cursor.close()

        except mysql.connector.Error as e:
            print(f"Migration warning: {e}")
