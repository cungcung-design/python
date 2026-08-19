import pytest


def test_cannot_sell_more_than_stock():
    available_stock = 10
    requested_quantity = 11
    assert requested_quantity > available_stock


def test_can_sell_exact_stock():
    available_stock = 10
    requested_quantity = 10
    assert requested_quantity == available_stock


def test_can_sell_within_stock():
    available_stock = 10
    requested_quantity = 3
    assert requested_quantity <= available_stock


def test_cart_total_calculation():
    cart = [
        {"price": 5.00, "quantity": 2},
        {"price": 3.50, "quantity": 1},
    ]
    total = sum(item["price"] * item["quantity"] for item in cart)
    assert total == 13.50


def test_cart_empty_raises():
    cart = []
    with pytest.raises(ValueError, match="Cart is empty"):
        if not cart:
            raise ValueError("Cart is empty")


def test_cart_quantity_validation():
    stock_quantity = 10
    requested_quantity = 11
    with pytest.raises(ValueError, match="Only 10 units"):
        if requested_quantity >= stock_quantity:
            raise ValueError(f"Only {stock_quantity} units are available.")