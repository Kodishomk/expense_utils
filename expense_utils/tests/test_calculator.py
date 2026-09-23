"""
Automated Test Suite for Expense Calculator
--------------------------------------------
Uses pytest to verify calculations, edge cases, and exception handling.
"""

import pytest
from expense_utils.calculator import (
    calculate_total,
    total_by_category,
    filter_by_category,
    check_budget_status,
)


@pytest.fixture
def sample_expenses():
    """Shared test fixture providing standard expense items."""
    return [
        {"description": "Groceries", "amount": 150.50, "category": "Food"},
        {"description": "Bus Fare", "amount": 25.00, "category": "Transport"},
        {"description": "Dinner", "amount": 45.50, "category": "Food"},
        {"description": "Movie Ticket", "amount": 15.00, "category": "Entertainment"},
    ]


# --- Test 1: Normal Total Calculation ---
def test_calculate_total_normal(sample_expenses):
    total = calculate_total(sample_expenses)
    assert total == 236.00


# --- Test 2: Edge Case - Empty Expenses ---
def test_calculate_total_empty():
    assert calculate_total([]) == 0.0


# --- Test 3: Normal Category Breakdown ---
def test_total_by_category(sample_expenses):
    totals = total_by_category(sample_expenses)
    assert totals == {"Food": 196.00, "Transport": 25.00, "Entertainment": 15.00}


# --- Test 4: Case-Insensitive Category Filtering ---
def test_filter_by_category(sample_expenses):
    food_items = filter_by_category(sample_expenses, "food")
    assert len(food_items) == 2
    assert all(item["category"] == "Food" for item in food_items)


# --- Test 5: Budget Status Evaluation ---
def test_check_budget_status(sample_expenses):
    status = check_budget_status(sample_expenses, 300.00)
    assert status["total_spent"] == 236.00
    assert status["remaining"] == 64.00
    assert status["is_over_budget"] is False

    over_status = check_budget_status(sample_expenses, 200.00)
    assert over_status["is_over_budget"] is True
    assert over_status["remaining"] == -36.00


# --- Test 6: Edge Case - Negative Amounts Raise ValueError ---
def test_negative_amount_raises_error():
    invalid_expenses = [{"description": "Refund Error", "amount": -50.00, "category": "Food"}]
    with pytest.raises(ValueError, match="Expense amount cannot be negative"):
        calculate_total(invalid_expenses)


# --- Test 7: Edge Case - Negative Budget Limit Raises ValueError ---
def test_negative_budget_raises_error(sample_expenses):
    with pytest.raises(ValueError, match="Budget limit cannot be negative"):
        check_budget_status(sample_expenses, -100.00)