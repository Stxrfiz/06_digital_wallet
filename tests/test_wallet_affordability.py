"""Unit tests for can_afford() in wallet_affordability.py (Spec section 3.2)."""
import pytest

from wallet_affordability import can_afford


# ---------- Decision logic: affordable or not ----------
@pytest.mark.parametrize(
    "balance, price, expected",
    [
        (1000, 500, True),   # balance above price
        (500, 500, True),    # boundary: balance equal to price
        (499, 500, False),   # boundary: one cent short
        (0, 1, False),       # empty wallet, non-zero price
        (1000, 0, True),     # zero price is affordable
        (0, 0, True),        # zero price with zero balance is affordable
    ],
    ids=["above_price", "equal_price", "one_cent_short", "empty_wallet", "zero_price", "zero_price_zero_balance"],
)
def test_can_afford_decision(balance, price, expected):
    assert can_afford(balance, price) == expected


# ---------- Output must be the real bool, not 1 or 0 ----------
@pytest.mark.parametrize(
    "balance, price, expected",
    [
        (1000, 500, True),
        (499, 500, False),
    ],
    ids=["returns_True", "returns_False"],
)
def test_can_afford_returns_actual_bool(balance, price, expected):
    assert can_afford(balance, price) is expected


# ---------- Out of range values: ValueError ----------
@pytest.mark.parametrize(
    "balance, price",
    [
        (-1, 0),   # negative balance
        (0, -1),   # negative price
    ],
    ids=["negative_balance", "negative_price"],
)
def test_can_afford_out_of_range_raises_value_error(balance, price):
    with pytest.raises(ValueError):
        can_afford(balance, price)


# ---------- Wrong data types: TypeError ----------
@pytest.mark.parametrize(
    "balance, price",
    [
        (1000.0, 500),  # float balance
        (1000, "500"),  # string price
        (True, 0),      # bool is not a valid int
        (1000, None),   # missing value
    ],
    ids=["float_balance", "str_price", "bool_balance", "none_price"],
)
def test_can_afford_wrong_type_raises_type_error(balance, price):
    with pytest.raises(TypeError):
        can_afford(balance, price)
