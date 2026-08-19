import pytest
from decimal import Decimal
from unittest.mock import MagicMock

from services.sales_service import SalesService


class FakeSalesDatabase:
    def __init__(self):
        self.items = {
            1: {"stock": 10, "price": Decimal("5.00")},
            2: {"stock": 5, "price": Decimal("3.50")},
        }
        self.sales = []
        self.safe_transactions = []
        self.committed = False
        self.rolled_back = False

    def begin_transaction(self):
        pass

    def fetch_all(self, query, params=None):
        normalized = " ".join(query.lower().split())
        if "from items" in normalized and "where id" in normalized:
            item_id = params[0] if params else None
            if item_id in self.items:
                return [(self.items[item_id]["stock"], self.items[item_id]["price"])]
            return []
        return []

    def execute_query(self, query, params=None):
        query_lower = query.lower()
        if "insert into sales" in query_lower:
            self.sales.append({
                "items_id": params[0],
                "quantity": params[1],
                "total": params[2],
                "user_id": params[4],
                "payment_method": params[5],
            })
            return MagicMock(lastrowid=len(self.sales))
        elif "update items" in query_lower:
            item_id = params[1]
            quantity = params[0]
            if item_id in self.items:
                self.items[item_id]["stock"] -= quantity
        elif "insert into safe_transactions" in query_lower:
            self.safe_transactions.append({
                "amount": params[0],
                "type": params[1],
                "staff_id": params[3],
            })
        return MagicMock()

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True


def test_checkout_success():
    db = FakeSalesDatabase()
    service = SalesService(db)

    cart = [
        {"id": 1, "name": "Coffee", "price": 5.00, "quantity": 2},
    ]

    result = service.checkout(cart, user_id=1, payment_method="Cash")

    assert result["sale_id"] == 1
    assert result["total"] == 10.0
    assert db.committed is True
    assert db.rolled_back is False
    assert db.items[1]["stock"] == 8


def test_checkout_empty_cart_raises():
    db = FakeSalesDatabase()
    service = SalesService(db)

    with pytest.raises(ValueError, match="Cart is empty"):
        service.checkout([], user_id=1, payment_method="Cash")


def test_checkout_insufficient_stock_raises():
    db = FakeSalesDatabase()
    service = SalesService(db)

    cart = [
        {"id": 2, "name": "Bread", "price": 3.50, "quantity": 10},
    ]

    with pytest.raises(ValueError, match="Insufficient stock"):
        service.checkout(cart, user_id=1, payment_method="Cash")

    assert db.rolled_back is True
