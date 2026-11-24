import pytest

from src.wallet_affordability import can_afford


# Valid inputs: the function must return the actual bool True or False,
# so "is" is used instead of "==" (1 == True would wrongly pass).
@pytest.mark.parametrize(("balance_cents", "price_cents", "expected"), [
    pytest.param(1000, 500, True, id="DW-AFF-TC-001"),   # balance above price
    pytest.param(500, 500, True, id="DW-AFF-TC-002"),    # balance equals price
    pytest.param(499, 500, False, id="DW-AFF-TC-003"),   # balance one cent below price
    pytest.param(1000, 0, True, id="DW-AFF-TC-004"),     # zero price
    pytest.param(0, 0, True, id="DW-AFF-TC-005"),        # zero price and zero balance
    pytest.param(0, 1, False, id="DW-AFF-TC-006"),       # zero balance cannot cover a price
])
def test_can_afford_with_valid_values_returns_bool(balance_cents, price_cents, expected):
    # Act
    result = can_afford(balance_cents, price_cents)
    # Assert
    assert result is expected


# Correct data type but outside the permitted range: ValueError.
@pytest.mark.parametrize(("balance_cents", "price_cents"), [
    pytest.param(-1, 0, id="DW-AFF-TC-007"),     # negative balance
    pytest.param(100, -1, id="DW-AFF-TC-008"),   # negative price
])
def test_can_afford_with_negative_value_raises_value_error(balance_cents, price_cents):
    # Act and Assert
    with pytest.raises(ValueError):
        can_afford(balance_cents, price_cents)


# Invalid data type: TypeError. bool is not a valid int.
@pytest.mark.parametrize(("balance_cents", "price_cents"), [
    pytest.param(10.5, 5, id="DW-AFF-TC-009"),    # float balance
    pytest.param(100, "50", id="DW-AFF-TC-010"),  # string price
    pytest.param(True, 0, id="DW-AFF-TC-011"),    # bool balance
    pytest.param(100, False, id="DW-AFF-TC-012"), # bool price
])
def test_can_afford_with_invalid_type_raises_type_error(balance_cents, price_cents):
    # Act and Assert
    with pytest.raises(TypeError):
        can_afford(balance_cents, price_cents)
