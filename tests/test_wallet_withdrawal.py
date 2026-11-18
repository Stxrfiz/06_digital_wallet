"""Unit tests for withdraw() in wallet_withdrawal.py (Spec section 3.1)."""
import pytest

from wallet_withdrawal import withdraw


# ---------- Valid withdrawals: correct remaining balance ----------
@pytest.mark.parametrize(
    "balance, amount, expected",
    [
        (1000, 300, 700),   # typical withdrawal
        (1000, 1, 999),     # boundary: smallest valid amount
        (1000, 999, 1),     # boundary: one cent below balance
        (1000, 1000, 0),    # boundary: exact balance is allowed, returns 0
        (1, 1, 0),          # boundary: smallest balance, exact withdrawal
    ],
    ids=["typical", "min_amount", "just_below_balance", "exact_balance", "exact_balance_one_cent"],
)
def test_withdraw_returns_remaining_balance(balance, amount, expected):
    assert withdraw(balance, amount) == expected


def test_withdraw_returns_int():
    assert type(withdraw(1000, 300)) is int


# ---------- Out of range values: ValueError ----------
@pytest.mark.parametrize(
    "balance, amount",
    [
        (-1, 1),       # negative balance
        (1000, 0),     # zero amount
        (1000, -1),    # negative amount
        (1000, 1001),  # amount just above balance
        (0, 1),        # nothing to withdraw from
    ],
    ids=["negative_balance", "zero_amount", "negative_amount", "above_balance", "zero_balance"],
)
def test_withdraw_out_of_range_raises_value_error(balance, amount):
    with pytest.raises(ValueError):
        withdraw(balance, amount)


# ---------- Wrong data types: TypeError ----------
@pytest.mark.parametrize(
    "balance, amount",
    [
        (1000.0, 100),   # float balance
        (1000, "100"),   # string amount
        (True, 1),       # bool is not a valid int
        (1000, True),    # bool is not a valid int
        (None, 100),     # missing value
    ],
    ids=["float_balance", "str_amount", "bool_balance", "bool_amount", "none_balance"],
)
def test_withdraw_wrong_type_raises_type_error(balance, amount):
    with pytest.raises(TypeError):
        withdraw(balance, amount)
