from database.database import Database
from models.staff import Staff


class ReportService:
    def __init__(self, db=None):
        self.db = db or Database()

    def get_today_sales(self):
        result = self.db.fetch_all(
            """
            SELECT COALESCE(SUM(total), 0)
            FROM sales
            WHERE DATE(date) = CURDATE()
            """
        )
        return float(result[0][0])

    def get_today_transactions(self):
        result = self.db.fetch_all(
            """
            SELECT COUNT(*)
            FROM sales
            WHERE DATE(date) = CURDATE()
            """
        )
        return int(result[0][0])

    def get_total_products(self):
        result = self.db.fetch_all(
            """
            SELECT COUNT(*)
            FROM items
            """
        )
        return int(result[0][0])

    def get_low_stock_products(self, threshold=10):
        return self.db.fetch_all(
            """
            SELECT
                id,
                name,
                stock_quantity
            FROM items
            WHERE stock_quantity <= %s
            ORDER BY stock_quantity ASC
            """,
            (threshold,),
        )

    def get_low_stock_count(self, threshold=10):
        result = self.db.fetch_all(
            """
            SELECT COUNT(*)
            FROM items
            WHERE stock_quantity <= %s
            """,
            (threshold,),
        )
        return result[0][0] if result else 0

    def get_sales_report(self):
        query = """
            SELECT
                s.id,
                i.name AS item_name,
                s.quantity,
                s.total,
                s.date,
                s.user_id
            FROM sales s
            LEFT JOIN items i
                ON s.items_id = i.id
            ORDER BY s.date DESC
        """
        return self.db.fetch_all(query)

    def get_today_transaction_count(self):
        result = self.db.fetch_all(
            """
            SELECT COUNT(*)
            FROM sales
            WHERE DATE(date) = CURDATE()
            """
        )
        return int(result[0][0]) if result else 0

    def get_dashboard_stats(self):
        today_sales = self.db.fetch_all(
            """
            SELECT COALESCE(SUM(total), 0)
            FROM sales
            WHERE DATE(date) = CURDATE()
            """
        )
        today_transactions = self.db.fetch_all(
            """
            SELECT COUNT(*)
            FROM sales
            WHERE DATE(date) = CURDATE()
            """
        )
        total_products = self.db.fetch_all(
            """
            SELECT COUNT(*)
            FROM items
            """
        )
        return {
            "today_sales": float(today_sales[0][0]) if today_sales else 0,
            "today_transactions": int(today_transactions[0][0]) if today_transactions else 0,
            "total_products": int(total_products[0][0]) if total_products else 0,
        }

    def get_recent_sales(self, limit=10):
        query = """
            SELECT
                s.id,
                i.name,
                s.quantity,
                s.total,
                s.date
            FROM sales s
            LEFT JOIN items i
                ON s.items_id = i.id
            ORDER BY s.date DESC
            LIMIT %s
        """
        return self.db.fetch_all(query, (limit,))

    def get_top_selling_products(self, limit=5):
        query = """
            SELECT
                i.name,
                SUM(s.quantity) AS quantity_sold,
                SUM(s.total) AS revenue
            FROM sales s
            LEFT JOIN items i
                ON s.items_id = i.id
            GROUP BY s.items_id, i.name
            ORDER BY quantity_sold DESC
            LIMIT %s
        """
        return self.db.fetch_all(query, (limit,))

    def get_all_staff(self) -> list:
        return self.db.fetch_all("SELECT id, name, role FROM staff")

    def get_staff_by_id(self, staff_id: int) -> Staff | None:
        row = self.db.fetch_all("SELECT id, name, role FROM staff WHERE id = %s", (staff_id,))
        if row:
            return Staff(id=row[0][0], name=row[0][1], role=row[0][2])
        return None

    def create_staff(self, name: str, role: str):
        self.db.execute_query("INSERT INTO staff (name, role) VALUES (%s, %s)", (name, role))

    def update_staff(self, staff_id: int, name: str, role: str):
        self.db.execute_query("UPDATE staff SET name = %s, role = %s WHERE id = %s", (name, role, staff_id))

    def delete_staff(self, staff_id: int):
        self.db.execute_query("DELETE FROM staff WHERE id = %s", (staff_id,))

    def get_sales_summary(self, days=30):
        return self.db.fetch_all(
            """
            SELECT
                DATE(date) AS sale_date,
                COALESCE(SUM(total), 0) AS total_sales,
                COUNT(*) AS transactions
            FROM sales
            WHERE date >= DATE_SUB(CURDATE(), INTERVAL %s DAY)
            GROUP BY DATE(date)
            ORDER BY sale_date
            """,
            (days,),
        )

    def get_best_selling_products(self, limit=10):
        return self.db.fetch_all(
            """
            SELECT
                i.name,
                SUM(s.quantity) AS quantity_sold,
                SUM(s.total) AS revenue
            FROM sales s
            JOIN items i
                ON s.items_id = i.id
            GROUP BY i.id, i.name
            ORDER BY quantity_sold DESC
            LIMIT %s
            """,
            (limit,),
        )

    def get_payment_summary(self):
        return self.db.fetch_all(
            """
            SELECT
                payment_method,
                COUNT(*) AS transactions,
                COALESCE(SUM(total), 0) AS total
            FROM sales
            GROUP BY payment_method
            ORDER BY total DESC
            """
        )

    def get_today_summary(self):
        result = self.db.fetch_all(
            """
            SELECT
                COALESCE(SUM(total), 0),
                COUNT(*)
            FROM sales
            WHERE DATE(date) = CURDATE()
            """
        )
        return result[0] if result else (0, 0)
