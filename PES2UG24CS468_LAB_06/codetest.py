import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


def test_invalid_cart():
    with pytest.raises(ValueError):
        coupon_discount("WELCOME10", 0, True, "mon")


def test_welcome():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


def test_weekend():
    assert coupon_discount("WEEKEND20", 600, True, "sat") == 120
    assert coupon_discount("WEEKEND20", 400, False, "sun") == 50
    assert coupon_discount("WEEKEND20", 600, True, "mon") == 0


def test_flat():
    assert coupon_discount("FLAT100", 500, True, "mon") == 100
    assert coupon_discount("FLAT100", 300, True, "mon") == 0


def test_unknown():
    assert coupon_discount("INVALID", 200, True, "mon") == 0


def test_best_discount():
    assert best_discount([], 200, True, "mon") == 0
    assert best_discount(["WELCOME10", "FLAT100"], 500, True, "mon") == 100
    assert best_discount(["WEEKEND20"], 100, True, "sat") == 40


def test_expiration():
    assert is_expired(10, 5, 0) is True
    assert is_expired(10, 5, -1) is True
    assert is_expired(16, 5, 10) is True
    assert is_expired(15, 5, 10) is False
    assert is_expired(10, 5, 10) is False
