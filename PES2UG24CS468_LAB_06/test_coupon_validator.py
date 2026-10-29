import pytest
from coupon_validator import coupon_discount, best_discount, is_expired

# Example test cases:
def test_welcome_coupon_new_user():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20

def test_zero_validity_expired():
    assert is_expired(10, 5, 0) is True
