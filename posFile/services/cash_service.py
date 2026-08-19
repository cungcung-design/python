from database.database import Database


class CashService:
    def __init__(self, db: Database, audit_service=None):
        self.db = db
        self.audit_service = audit_service

    def open_register(self, staff_id: int, opening_cash: float, user_id=None):
        try:
            self.db.execute_query(
                """
                INSERT INTO cash_registers
                    (staff_id, opening_cash, status)
                VALUES (%s, %s, 'open')
                """,
                (staff_id, opening_cash),
            )
            if self.audit_service and user_id:
                self.audit_service.log(
                    user_id,
                    "REGISTER_OPENED",
                    "CashRegister",
                    None,
                    f"Register opened with RM{opening_cash:.2f}",
                )
            return self.get_open_register(staff_id)
        except Exception:
            return None

    def get_open_register(self, staff_id: int):
        try:
            rows = self.db.fetch_all(
                """
                SELECT id, opening_cash
                FROM cash_registers
                WHERE staff_id = %s
                  AND status = 'open'
                ORDER BY id DESC
                LIMIT 1
                """,
                (staff_id,),
            )
            if rows:
                return rows[0]
            return None
        except Exception:
            return None

    def get_sales_total(self, user_id: int):
        try:
            rows = self.db.fetch_all(
                """
                SELECT COALESCE(SUM(total), 0)
                FROM sales
                WHERE user_id = %s
                  AND DATE(date) = CURDATE()
                """,
                (user_id,),
            )
            return float(rows[0][0])
        except Exception:
            return 0.0

    def get_cash_movements(self, staff_id: int):
        try:
            rows = self.db.fetch_all(
                """
                SELECT type, COALESCE(SUM(amount), 0)
                FROM safe_transactions
                WHERE staff_id = %s
                GROUP BY type
                """,
                (staff_id,),
            )
            cash_in = 0.0
            cash_out = 0.0
            for row in rows:
                type_value = str(row[0]).lower()
                amount = float(row[1])
                if type_value in ("in", "deposit", "cash_in"):
                    cash_in += amount
                elif type_value in ("out", "withdraw", "cash_out"):
                    cash_out += amount
            return cash_in, cash_out
        except Exception:
            return 0.0, 0.0

    def calculate_expected_cash(self, user_id: int, staff_id: int):
        register = self.get_open_register(staff_id)
        if not register:
            return 0.0
        opening_cash = float(register[1])
        sales = self.get_sales_total(user_id)
        cash_in, cash_out = self.get_cash_movements(staff_id)
        return opening_cash + sales + cash_in - cash_out

    def close_register(self, user_id: int, staff_id: int, actual_cash: float):
        register = self.get_open_register(staff_id)
        if not register:
            return None
        expected_cash = self.calculate_expected_cash(user_id, staff_id)
        difference = actual_cash - expected_cash
        try:
            self.db.execute_query(
                """
                UPDATE cash_registers
                SET
                    closing_cash = %s,
                    expected_cash = %s,
                    difference = %s,
                    closed_at = NOW(),
                    status = 'closed'
                WHERE id = %s
                """,
                (
                    actual_cash,
                    expected_cash,
                    difference,
                    register[0],
                ),
            )
            if self.audit_service and user_id:
                self.audit_service.log(
                    user_id,
                    "REGISTER_CLOSED",
                    "CashRegister",
                    register[0],
                    f"Register closed. Expected: RM{expected_cash:.2f}, Actual: RM{actual_cash:.2f}, Difference: RM{difference:.2f}",
                )
            return {
                "expected": expected_cash,
                "actual": actual_cash,
                "difference": difference,
            }
        except Exception:
            return None
