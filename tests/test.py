import pytest

from budgeting_recommender.main import BudgetTracker


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
