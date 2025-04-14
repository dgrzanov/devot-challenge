from datetime import date, timedelta
from typing import Any, Optional

from fastapi import APIRouter, Query
from sqlmodel import select

from deps import CurrentUser, SessionDep
from expenses.expenses_models import Expense
from report.report_models import ReportByPeriod

router = APIRouter(tags=["report"])


@router.get("/by-period", response_model=ReportByPeriod)
def report_by_period(
    session: SessionDep,
    current_user: CurrentUser,
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
) -> Any:
    """
    Get expenses.
    """

    filters = [Expense.user_id == current_user.id]

    if start_date:
        filters.append(Expense.date >= start_date)
    if end_date:
        filters.append(Expense.date < end_date + timedelta(days=1))

    statement = select(Expense).where(*filters)
    expenses = session.exec(statement).all()

    spent_by_category = {}
    for expense in expenses:
        if expense.category:
            spent_by_category[expense.category.name] = (
                spent_by_category.get(expense.category.name, 0) + expense.amount
            )

    return ReportByPeriod(
        total_spent=sum(expense.amount for expense in expenses),
        total_expenses=len(expenses),
        average_spent=(
            sum(expense.amount for expense in expenses) / len(expenses)
            if expenses
            else 0
        ),
        start_date=start_date,
        end_date=end_date,
        user_id=current_user.id,
        spent_by_category=spent_by_category,
    )
