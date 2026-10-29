import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


def test_invalid_cart():
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", 0, True, "mon")


def test_welcome_branches():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0


def test_weekend_branches():
    assert coupon_discount("WEEKEND20", 600, True, "sat") == 120
    assert coupon_discount("WEEKEND20", 400, True, "sun") == 50
    assert coupon_discount("WEEKEND20", 600, True, "mon") == 0


def test_flat_branches():
    assert coupon_discount("FLAT100", 500, True, "mon") == 100
    assert coupon_discount("FLAT100", 300, True, "mon") == 0


def test_unknown_coupon():
    assert coupon_discount("INVALID", 200, True, "mon") == 0


def test_best_discount_branches():
    assert best_discount([], 100, True, "mon") == 0
    assert best_discount(["WELCOME10"], 100, True, "mon") == 10
    assert best_discount(["WEEKEND20"], 100, True, "sat") == 40


def test_expiration_branches():
    assert is_expired(10, 5, 0) is True
    assert is_expired(16, 5, 10) is True
    assert is_expired(15, 5, 10) is False
