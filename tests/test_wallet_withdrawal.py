#demo
import pytest

from src.wallet_withdrawal import withdraw


# Valid withdrawals: the remaining balance is returned in cents.
@pytest.mark.parametrize(("balance_cents", "amount_cents", "expected_balance"), [
    pytest.param(1000, 300, 700, id="DW-WDR-TC-001"),   # normal withdrawal
    pytest.param(1000, 1, 999, id="DW-WDR-TC-002"),     # smallest valid amount
    pytest.param(1000, 999, 1, id="DW-WDR-TC-003"),     # one cent below the balance
    pytest.param(1000, 1000, 0, id="DW-WDR-TC-004"),    # exact balance returns zero
])
def test_withdraw_with_valid_amount_returns_remaining_balance(balance_cents, amount_cents, expected_balance):
    # Act
    result = withdraw(balance_cents, amount_cents)
    # Assert
    assert result == expected_balance


# Correct data type but outside the permitted range: ValueError.
@pytest.mark.parametrize(("balance_cents", "amount_cents"), [
    pytest.param(1000, 0, id="DW-WDR-TC-005"),      # zero amount
    pytest.param(1000, -100, id="DW-WDR-TC-006"),   # negative amount
    pytest.param(-1, 1, id="DW-WDR-TC-007"),        # negative balance
    pytest.param(1000, 1001, id="DW-WDR-TC-008"),   # one cent above the balance
    pytest.param(0, 1, id="DW-WDR-TC-009"),         # withdrawal from a zero balance
])
def test_withdraw_with_out_of_range_value_raises_value_error(balance_cents, amount_cents):
    # Act and Assert
    with pytest.raises(ValueError):
        withdraw(balance_cents, amount_cents)


# Invalid data type: TypeError. bool is not a valid int.
@pytest.mark.parametrize(("balance_cents", "amount_cents"), [
    pytest.param(1000.0, 300, id="DW-WDR-TC-010"),   # float balance
    pytest.param(1000, "300", id="DW-WDR-TC-011"),   # string amount
    pytest.param(True, 1, id="DW-WDR-TC-012"),       # bool balance
    pytest.param(1000, True, id="DW-WDR-TC-013"),    # bool amount
])
def test_withdraw_with_invalid_type_raises_type_error(balance_cents, amount_cents):
    # Act and Assert
    with pytest.raises(TypeError):
        withdraw(balance_cents, amount_cents)
