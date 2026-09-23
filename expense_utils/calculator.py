"""
Expense Calculator Engine
-------------------------
Pure functions for processing, filtering, and aggregating financial expenses.
"""

from typing import Dict, List, Any


def calculate_total(expenses: List[Dict[str, Any]]) -> float:
    """Calculates the total amount across all expenses."""
    if not expenses:
        return 0.0

    total = 0.0
    for item in expenses:
        amount = item.get("amount", 0.0)
        if amount < 0:
            raise ValueError(f"Expense amount cannot be negative: {amount}")
        total +=float(amount)
    return round(total, 2)


def total_by_category(expenses: List[Dict[str, Any]]) -> Dict[str, float]:
    """Aggregates total expenses grouped by category."""
    category_totals: Dict[str, float] = {}

    for item in expenses:
        category = item.get("category", "Uncategorized").strip().title()
        amount = item.get("amount", 0.0)

        if amount < 0:
            raise ValueError(f"Expense amount cannot be negative: {amount}")

        category_totals[category] = round(
            category_totals.get(category, 0.0) + float(amount), 2
        )

    return category_totals


def filter_by_category(
    expenses: List[Dict[str, Any]], category: str
) -> List[Dict[str, Any]]:
    """Filters expenses by a specific category (case-insensitive)."""
    target = category.strip().lower()
    return [
        item
        for item in expenses
        if item.get("category", "").strip().lower() == target
    ]


def check_budget_status(
    expenses: List[Dict[str, Any]], budget_limit: float
) -> Dict[str, Any]:
    """
    Evaluates total spending against a budget limit.
    Returns summary dict with total, remaining budget, and over-budget flag.
    """
    if budget_limit < 0:
        raise ValueError("Budget limit cannot be negative.")

    total_spent = calculate_total(expenses)
    remaining = round(budget_limit - total_spent, 2)
    is_over = total_spent > budget_limit

    return {
        "total_spent": total_spent,
        "budget_limit": budget_limit,
        "remaining": remaining,
        "is_over_budget": is_over,
    }