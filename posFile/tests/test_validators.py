from utils.validators import (
    required,
    positive_number,
    positive_integer,
)


def test_required_rejects_none():
    result = required(None, "Product name")
    assert result is not None


def test_required_rejects_empty_string():
    result = required("", "Product name")
    assert result is not None


def test_required_accepts_value():
    result = required("Coffee", "Product name")
    assert result is None


def test_positive_number_accepts_valid_price():
    result = positive_number("5.50", "Price")
    assert result is None


def test_positive_number_rejects_text():
    result = positive_number("abc", "Price")
    assert result is not None


def test_positive_integer_rejects_negative():
    result = positive_integer("-5", "Stock")
    assert result is not None


def test_positive_integer_accepts_valid_stock():
    result = positive_integer("20", "Stock")
    assert result is None
