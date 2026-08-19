from unittest.mock import MagicMock

from services.cash_service import CashService


class FakeCashDatabase:
    def __init__(self):
        self.cash_registers = []
        self.safe_transactions = []
        self.sales = []
        self.next_register_id = 1

    def fetch_all(self, query, params=None):
        normalized = " ".join(query.lower().split())
        if "from cash_registers" in normalized and "where staff_id" in normalized:
            staff_id = params[0]
            open_registers = [
                (r["id"], r["opening_cash"])
                for r in self.cash_registers
                if r["staff_id"] == staff_id and r["status"] == "open"
            ]
            return open_registers
        if "coalesce(sum(total), 0)" in normalized and "from sales" in normalized:
            user_id = params[0]
            return [(sum(t[0] for t in self.sales if t[3] == user_id),)]
        if "from safe_transactions" in normalized and "group by type" in normalized:
            staff_id = params[0]
            cash_in = sum(t[0] for t in self.safe_transactions if t[2] == staff_id and t[1] in ("in", "deposit", "cash_in"))
            cash_out = sum(t[0] for t in self.safe_transactions if t[2] == staff_id and t[1] in ("out", "withdraw", "cash_out"))
            result = []
            if cash_in:
                result.append(("in", cash_in))
            if cash_out:
                result.append(("out", cash_out))
            return result
        return []

    def execute_query(self, query, params=None):
        query_lower = query.lower()
        if "insert into cash_registers" in query_lower:
            register_id = self.next_register_id
            self.cash_registers.append({
                "id": register_id,
                "staff_id": params[0],
                "opening_cash": params[1],
                "status": "open",
            })
            self.next_register_id += 1
            return MagicMock()
        elif "update cash_registers" in query_lower:
            for register in self.cash_registers:
                if register["id"] == params[3]:
                    register["closing_cash"] = params[0]
                    register["expected_cash"] = params[1]
                    register["difference"] = params[2]
                    register["status"] = "closed"
        return MagicMock()


def test_open_register():
    db = FakeCashDatabase()
    service = CashService(db)
    result = service.open_register(staff_id=1, opening_cash=200.0)
    assert result is not None
    assert len(db.cash_registers) == 1


def test_get_open_register():
    db = FakeCashDatabase()
    service = CashService(db)
    db.cash_registers.append({
        "id": 1,
        "staff_id": 1,
        "opening_cash": 200.0,
        "status": "open",
    })
    register = service.get_open_register(staff_id=1)
    assert register is not None
    assert register[0] == 1
    assert register[1] == 200.0


def test_get_open_register_none():
    db = FakeCashDatabase()
    service = CashService(db)
    register = service.get_open_register(staff_id=1)
    assert register is None


def test_calculate_expected_cash():
    db = FakeCashDatabase()
    service = CashService(db)
    db.cash_registers.append({
        "id": 1,
        "staff_id": 1,
        "opening_cash": 200.0,
        "status": "open",
    })
    db.sales.append((350.0, None, None, 1))
    db.safe_transactions.append((50.0, "in", 1))
    db.safe_transactions.append((20.0, "out", 1))
    expected = service.calculate_expected_cash(user_id=1, staff_id=1)
    assert expected == 580.0


def test_close_register():
    db = FakeCashDatabase()
    service = CashService(db)
    db.cash_registers.append({
        "id": 1,
        "staff_id": 1,
        "opening_cash": 200.0,
        "status": "open",
    })
    db.sales.append((350.0, None, None, 1))
    db.safe_transactions.append((50.0, "in", 1))
    db.safe_transactions.append((20.0, "out", 1))
    result = service.close_register(user_id=1, staff_id=1, actual_cash=570.0)
    assert result is not None
    assert result["actual"] == 570.0
    assert result["difference"] == -10.0


def test_close_register_no_open():
    db = FakeCashDatabase()
    service = CashService(db)
    result = service.close_register(user_id=1, staff_id=1, actual_cash=570.0)
    assert result is None