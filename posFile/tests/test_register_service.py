def test_register_expected_cash():
    opening = 200
    sales = 350
    cash_in = 50
    cash_out = 20
    expected = opening + sales + cash_in - cash_out
    assert expected == 580


def test_register_difference():
    expected = 580
    actual = 570
    difference = actual - expected
    assert difference == -10


def test_register_exact_match():
    expected = 580
    actual = 580
    difference = actual - expected
    assert difference == 0


def test_register_positive_difference():
    expected = 500
    actual = 520
    difference = actual - expected
    assert difference == 20