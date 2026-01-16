import pytest

from main import BudgetTracker


@pytest.mark.parametrize(
    "initial_tx_count, expected_tx_count",
    [
        pytest.param(0, 0, id="happy_path_zero_transactions"),
        pytest.param(1, 1, id="happy_path_single_transaction"),
        pytest.param(5, 5, id="happy_path_multiple_transactions"),
        pytest.param(100, 100, id="happy_path_large_number_of_transactions"),
    ],
)
def test_get_tx_count_happy_path(initial_tx_count, expected_tx_count):
    # Arrange

    tracker = BudgetTracker()
    tracker.tx_count = initial_tx_count

    # Act

    result = tracker.get_tx_count()

    # Assert

    assert result == expected_tx_count


@pytest.mark.parametrize(
    "initial_tx_count, expected_tx_count",
    [
        pytest.param(0, 0, id="edge_zero_value"),
        pytest.param(10**6, 10**6, id="edge_very_large_value"),
        pytest.param(-1, -1, id="edge_negative_value_direct_assignment"),
    ],
)
def test_get_tx_count_edge_cases(initial_tx_count, expected_tx_count):
    # Arrange

    tracker = BudgetTracker()
    tracker.tx_count = initial_tx_count

    # Act

    result = tracker.get_tx_count()

    # Assert

    assert result == expected_tx_count


@pytest.mark.parametrize(
    "invalid_value, description",
    [
        pytest.param(None, "none_value", id="error_none_value"),
        pytest.param("3", "string_value", id="error_string_value"),
        pytest.param("Matt (or any name)", "string_value", id="error_string_value"),
        pytest.param(3.5, "float_value", id="error_float_value"),
        pytest.param([], "list_value", id="error_list_value"),
        pytest.param({}, "dict_value", id="error_dict_value"),
    ],
)
def test_get_tx_count_error_cases(invalid_value, description):
    # Arrange

    tracker = BudgetTracker()
    tracker.tx_count = invalid_value

    # Act

    result = tracker.get_tx_count()

    # Assert

    # get_tx_count simply returns the stored value without validation,
    # so the result should be exactly the invalid value assigned.
    assert result is invalid_value


# ==================== Transaction Management Tests ====================

class TestAddOneTransaction:
    def test_add_one_tx_increments_count(self):
        # Arrange
        tracker = BudgetTracker()
        initial_count = tracker.tx_count

        # Act
        tracker.add_one_tx()

        # Assert
        assert tracker.tx_count == initial_count + 1

    def test_add_one_tx_multiple_times(self):
        # Arrange
        tracker = BudgetTracker()

        # Act
        tracker.add_one_tx()
        tracker.add_one_tx()
        tracker.add_one_tx()

        # Assert
        assert tracker.tx_count == 3


class TestSubtractOneTransaction:
    def test_subtract_one_tx_decrements_count(self):
        # Arrange
        tracker = BudgetTracker()
        tracker.tx_count = 5

        # Act
        tracker.subtract_one_tx()

        # Assert
        assert tracker.tx_count == 4

    def test_subtract_one_tx_multiple_times(self):
        # Arrange
        tracker = BudgetTracker()
        tracker.tx_count = 10

        # Act
        tracker.subtract_one_tx()
        tracker.subtract_one_tx()
        tracker.subtract_one_tx()

        # Assert
        assert tracker.tx_count == 7

    def test_subtract_one_tx_at_zero_does_not_go_negative(self):
        # Arrange
        tracker = BudgetTracker()
        tracker.tx_count = 0

        # Act
        tracker.subtract_one_tx()

        # Assert
        assert tracker.tx_count == 0


class TestGetDepositCount:
    @pytest.mark.parametrize(
        "initial_deposits, expected_deposits",
        [
            pytest.param(0, 0, id="zero_deposits"),
            pytest.param(1, 1, id="single_deposit"),
            pytest.param(10, 10, id="multiple_deposits"),
        ],
    )
    def test_get_deposit_count_returns_correct_value(self, initial_deposits, expected_deposits):
        # Arrange
        tracker = BudgetTracker()
        tracker.deposits = initial_deposits

        # Act
        result = tracker.get_deposit_count()

        # Assert
        assert result == expected_deposits


class TestAddOneDeposit:
    def test_add_one_deposit_increments_count(self):
        # Arrange
        tracker = BudgetTracker()
        initial_count = tracker.deposits

        # Act
        tracker.add_one_deposit()

        # Assert
        assert tracker.deposits == initial_count + 1

    def test_add_one_deposit_multiple_times(self):
        # Arrange - initialize a BudgetTracker instance
        # By default, number of deposits is set to 0
        tracker = BudgetTracker()

        # Act
        tracker.add_one_deposit()
        tracker.add_one_deposit()
        tracker.add_one_deposit()

        # Assert
        assert tracker.deposits == 3


class TestSubtractOneDeposit:
    def test_subtract_one_deposit_decrements_count(self):
        # Arrange
        tracker = BudgetTracker()
        tracker.deposits = 5

        # Act
        tracker.subtract_one_deposit()
        tracker.subtract_one_deposit()
        tracker.subtract_one_deposit()

        # Assert
        assert tracker.deposits == 2

    def test_subtract_one_deposit_at_zero_does_not_go_negative(self):
        # Arrange
        tracker = BudgetTracker()
        tracker.deposits = 0

        # Act
        tracker.subtract_one_deposit()

        # Assert
        assert tracker.deposits == 0


# ==================== Income & Expense Operations Tests ====================

class TestAddIncome:
    def test_add_income_increases_total_income(self):
        # Arrange
        tracker = BudgetTracker()

        # Act
        tracker.add_income(100.0)

        # Assert
        assert tracker.income == 100.0

    def test_add_income_increments_deposit_count(self):
        # Arrange
        tracker = BudgetTracker()

        # Act
        tracker.add_income(100.0)

        # Assert
        assert tracker.get_deposit_count() == 1

    def test_add_income_records_transaction(self):
        # Arrange
        tracker = BudgetTracker()

        # Act
        tracker.add_income(100.0)

        # Assert
        assert 100.0 in tracker.each_transaction

    def test_add_income_accumulates_multiple_deposits(self):
        # Arrange
        tracker = BudgetTracker()

        # Act
        tracker.add_income(100.0)
        tracker.add_income(50.0)
        tracker.add_income(25.50)

        # Assert
        assert tracker.income == 175.50
        assert tracker.get_deposit_count() == 3
        assert len(tracker.each_transaction) == 3

    @pytest.mark.parametrize(
        "amount",
        [
            pytest.param(0.01, id="small_amount"),
            pytest.param(1000.0, id="large_amount"),
            pytest.param(0.0, id="zero_amount"),
        ],
    )
    def test_add_income_various_amounts(self, amount):
        # Arrange
        tracker = BudgetTracker()

        # Act
        tracker.add_income(amount)

        # Assert
        assert tracker.income == amount


class TestAddExpense:
    def test_add_expense_increases_total_expenses(self):
        # Arrange
        tracker = BudgetTracker()

        # Act
        tracker.add_expense(50.0)

        # Assert
        assert tracker.expenses == 50.0

    def test_add_expense_increments_transaction_count(self):
        # Arrange
        tracker = BudgetTracker()

        # Act
        tracker.add_expense(50.0)

        # Assert
        assert tracker.get_tx_count() == 1

    def test_add_expense_records_negative_transaction(self):
        # Arrange
        tracker = BudgetTracker()

        # Act
        tracker.add_expense(50.0)

        # Assert
        assert -50.0 in tracker.each_transaction

    def test_add_expense_accumulates_multiple_expenses(self):
        # Arrange
        tracker = BudgetTracker()

        # Act
        tracker.add_expense(25.0)
        tracker.add_expense(15.0)
        tracker.add_expense(10.50)

        # Assert
        assert tracker.expenses == 50.50
        assert tracker.get_tx_count() == 3
        assert len(tracker.each_transaction) == 3

    @pytest.mark.parametrize(
        "amount",
        [
            pytest.param(0.01, id="small_amount"),
            pytest.param(1000.0, id="large_amount"),
            pytest.param(0.0, id="zero_amount"),
        ],
    )
    def test_add_expense_various_amounts(self, amount):
        # Arrange
        tracker = BudgetTracker()

        # Act
        tracker.add_expense(amount)

        # Assert
        assert tracker.expenses == amount


class TestRemoveExpense:
    def test_remove_expense_decreases_total_expenses(self):
        # Arrange
        tracker = BudgetTracker()
        tracker.add_expense(100.0)

        # Act
        tracker.remove_expense(30.0)

        # Assert
        assert tracker.expenses == 70.0

    def test_remove_expense_decrements_transaction_count(self):
        # Arrange
        tracker = BudgetTracker()
        tracker.add_expense(100.0)

        # Act
        tracker.remove_expense(30.0)

        # Assert
        assert tracker.get_tx_count() == 0

    def test_remove_expense_with_multiple_expenses(self):
        # Arrange
        tracker = BudgetTracker()
        tracker.add_expense(50.0)
        tracker.add_expense(50.0)

        # Act
        tracker.remove_expense(25.0)

        # Assert
        assert tracker.expenses == 75.0
        assert tracker.get_tx_count() == 1

    def test_remove_expense_when_no_expenses_exist(self):
        # Arrange
        tracker = BudgetTracker()

        # Act
        tracker.remove_expense(50.0)

        # Assert
        assert tracker.expenses == 0
        assert tracker.get_tx_count() == 0

    def test_remove_expense_when_tx_count_is_zero(self):
        # Arrange
        tracker = BudgetTracker()
        tracker.expenses = 100.0
        tracker.tx_count = 0

        # Act
        tracker.remove_expense(50.0)

        # Assert
        # Should not remove when tx_count is 0
        assert tracker.expenses == 100.0


# ==================== Budget Calculation Tests ====================

class TestViewBudget:
    def test_view_budget_with_only_income(self):
        # Arrange
        tracker = BudgetTracker()
        tracker.add_income(1000.0)

        # Act & Assert
        balance = tracker.income - tracker.expenses
        assert balance == 1000.0

    def test_view_budget_with_only_expenses(self):
        # Arrange
        tracker = BudgetTracker()
        tracker.add_expense(500.0)

        # Act & Assert
        balance = tracker.income - tracker.expenses
        assert balance == -500.0

    def test_view_budget_with_income_and_expenses(self):
        # Arrange
        tracker = BudgetTracker()
        tracker.add_income(1000.0)
        tracker.add_expense(300.0)
        tracker.add_expense(200.0)

        # Act & Assert
        balance = tracker.income - tracker.expenses
        assert balance == 500.0

    def test_view_budget_accurate_calculations(self):
        # Arrange
        tracker = BudgetTracker()
        tracker.add_income(2500.0)
        tracker.add_income(1500.0)
        tracker.add_expense(1000.0)
        tracker.add_expense(500.0)

        # Act
        expected_balance = 4000.0 - 1500.0

        # Assert
        assert tracker.income == 4000.0
        assert tracker.expenses == 1500.0
        assert (tracker.income - tracker.expenses) == expected_balance


# ==================== State Management Tests ====================

class TestUserField:
    def test_user_field_can_be_set(self):
        # Arrange
        tracker = BudgetTracker()

        # Act
        tracker.user = "John Doe"

        # Assert
        assert tracker.user == "John Doe"

    def test_user_field_initially_empty(self):
        # Arrange & Act
        tracker = BudgetTracker()

        # Assert
        assert tracker.user == ""

    def test_user_field_can_be_changed(self):
        # Arrange
        tracker = BudgetTracker()
        tracker.user = "John Doe"

        # Act
        tracker.user = "Jane Smith"

        # Assert
        assert tracker.user == "Jane Smith"


# ==================== Initial State Tests ====================

class TestInitialState:
    def test_initial_state_all_counters_zero(self):
        # Arrange & Act
        tracker = BudgetTracker()

        # Assert
        assert tracker.tx_count == 0
        assert tracker.deposits == 0
        assert tracker.income == 0
        assert tracker.expenses == 0

    def test_initial_state_empty_lists(self):
        # Arrange & Act
        tracker = BudgetTracker()

        # Assert
        assert tracker.each_transaction == []

    def test_initial_state_user_empty(self):
        # Arrange & Act
        tracker = BudgetTracker()

        # Assert
        assert tracker.user == ""


# ==================== Integration Tests ====================

class TestIntegration:
    def test_mixed_income_and_expenses_workflow(self):
        # Arrange
        tracker = BudgetTracker()

        # Act
        tracker.add_income(5000.0)
        tracker.add_expense(1000.0)
        tracker.add_expense(500.0)
        tracker.add_income(2000.0)
        tracker.add_expense(200.0)

        # Assert
        assert tracker.income == 7000.0
        assert tracker.expenses == 1700.0
        assert tracker.get_deposit_count() == 2
        assert tracker.get_tx_count() == 3
        assert len(tracker.each_transaction) == 5
        assert (tracker.income - tracker.expenses) == 5300.0

    def test_transaction_list_contains_correct_signs(self):
        # Arrange
        tracker = BudgetTracker()

        # Act
        tracker.add_income(100.0)
        tracker.add_expense(50.0)
        tracker.add_income(75.0)

        # Assert
        assert tracker.each_transaction == [100.0, -50.0, 75.0]

    def test_remove_expense_after_adding_multiple(self):
        # Arrange
        tracker = BudgetTracker()
        tracker.add_expense(100.0)
        tracker.add_expense(50.0)
        tracker.add_expense(25.0)

        # Act
        tracker.remove_expense(30.0)

        # Assert
        assert tracker.expenses == 145.0
        assert tracker.get_tx_count() == 2
