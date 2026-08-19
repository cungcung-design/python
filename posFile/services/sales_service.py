from datetime import datetime
from database.database import Database
from models.sale import Sale
from models.staff import Staff


class SalesService:
    def __init__(self, db: Database, audit_service=None):
        self.db = db
        self.audit_service = audit_service

    def record_sale(self, item_id: int, quantity: int, total: float, staff_id: int) -> Sale:
        now = datetime.now()
        self.db.execute_query(
            """
            INSERT INTO sales (items_id, quantity, total, date, user_id, payment_method)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (item_id, quantity, total, now, staff_id, "Cash"),
        )
        return Sale(id=None, item_id=item_id, quantity=quantity, total=total, date=now, staff_id=staff_id)

    def record_payment(self, amount: float, staff_id: int):
        now = datetime.now()
        self.db.execute_query(
            """
            INSERT INTO safe_transactions (amount, type, date, staff_id)
            VALUES (%s, %s, %s, %s)
            """,
            (amount, "Payment", now, staff_id),
        )

    def get_all_transactions(self) -> list:
        return self.db.fetch_all("SELECT id, amount, type, date, staff_id FROM safe_transactions")

    def get_transactions_by_date(self, date_str: str) -> list:
        return self.db.fetch_all(
            "SELECT id, amount, type, date, staff_id FROM safe_transactions WHERE DATE(date) = %s",
            (date_str,),
        )

    def checkout(self, cart, user_id, payment_method="Cash"):
        if not cart:
            raise ValueError("Cart is empty.")

        self.db.begin_transaction()

        try:
            total = 0
            sale_ids = []

            for item in cart:
                result = self.db.fetch_all(
                    """
                    SELECT stock_quantity, price
                    FROM items
                    WHERE id = %s
                    FOR UPDATE
                    """,
                    (item["id"],),
                )

                if not result:
                    raise ValueError(f"Product {item['name']} does not exist.")

                stock = int(result[0][0])
                price = float(result[0][1])
                quantity = int(item["quantity"])

                if quantity > stock:
                    raise ValueError(
                        f"Insufficient stock for {item['name']}. Available: {stock}"
                    )

                item_total = price * quantity
                total += item_total

                cursor = self.db.execute_query(
                    """
                    INSERT INTO sales (items_id, quantity, total, date, user_id, payment_method)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        item["id"],
                        quantity,
                        item_total,
                        datetime.now(),
                        user_id,
                        payment_method,
                    ),
                )
                sale_ids.append(cursor.lastrowid)

                self.db.execute_query(
                    """
                    UPDATE items
                    SET stock_quantity = stock_quantity - %s
                    WHERE id = %s
                    """,
                    (quantity, item["id"]),
                )

            self.db.execute_query(
                """
                INSERT INTO safe_transactions (amount, type, date, staff_id)
                VALUES (%s, %s, %s, %s)
                """,
                (total, "Payment", datetime.now(), user_id),
            )

            self.db.commit()

            if self.audit_service:
                self.audit_service.log(
                    user_id,
                    "TRANSACTION_CREATED",
                    "Sale",
                    sale_ids[0] if sale_ids else None,
                    f"Transaction completed. Total: RM{total:.2f}, Payment: {payment_method}",
                )

            return {
                "sale_id": sale_ids[0] if sale_ids else None,
                "total": total,
                "items": list(cart),
            }

        except Exception as e:
            self.db.rollback()
            raise e
