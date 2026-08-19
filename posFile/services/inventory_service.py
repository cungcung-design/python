from database.database import Database


class InventoryService:
    def __init__(self, db: Database, audit_service=None):
        self.db = db
        self.audit_service = audit_service

    def add_stock(self, item_id: int, quantity: int, staff_id: int = None, note: str = "", user_id=None):
        connection = self.db.connection
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT stock_quantity FROM items WHERE id = %s", (item_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError("Item not found")

            old_quantity = row[0]
            new_quantity = old_quantity + quantity

            cursor.execute(
                "UPDATE items SET stock_quantity = %s WHERE id = %s",
                (new_quantity, item_id),
            )

            cursor.execute(
                """
                INSERT INTO stock_transactions
                    (item_id, quantity, type, note, staff_id)
                VALUES
                    (%s, %s, 'STOCK_IN', %s, %s)
                """,
                (item_id, quantity, note, staff_id),
            )

            connection.commit()

            if self.audit_service and user_id:
                self.audit_service.log(
                    user_id,
                    "STOCK_ADJUSTED",
                    "Product",
                    item_id,
                    f"Stock increased by {quantity}. New quantity: {new_quantity}",
                )

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()

    def adjust_stock(
        self,
        item_id: int,
        new_quantity: int,
        staff_id: int = None,
        note: str = "",
        user_id=None,
    ):
        connection = self.db.connection
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT stock_quantity FROM items WHERE id = %s", (item_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError("Item not found")

            old_quantity = row[0]
            difference = new_quantity - old_quantity

            cursor.execute(
                "UPDATE items SET stock_quantity = %s WHERE id = %s",
                (new_quantity, item_id),
            )

            cursor.execute(
                """
                INSERT INTO stock_transactions
                    (item_id, quantity, type, note, staff_id)
                VALUES
                    (%s, %s, 'ADJUSTMENT', %s, %s)
                """,
                (
                    item_id,
                    difference,
                    note,
                    staff_id,
                ),
            )

            connection.commit()

            if self.audit_service and user_id:
                self.audit_service.log(
                    user_id,
                    "STOCK_ADJUSTED",
                    "Product",
                    item_id,
                    f"Stock adjusted from {old_quantity} to {new_quantity}",
                )

        except Exception:
            connection.rollback()
            raise

        finally:
            cursor.close()

    def get_low_stock(self, threshold: int = 10):
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

    def get_inventory_value(self):
        result = self.db.fetch_all(
            """
            SELECT
                COALESCE(SUM(price * stock_quantity), 0)
            FROM items
            """
        )
        return float(result[0][0])
