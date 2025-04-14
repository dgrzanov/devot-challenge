from datetime import date, timedelta
from typing import Any, List, Optional

from fastapi import APIRouter, Query
from sqlmodel import func, select

from deps import CurrentUser, SessionDep
from expenses.expenses_models import Expense
from report.report_models import (
    AggregatedReport,
    ExpenseAggregate,
    GroupBy,
    ReportByPeriod,
)

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


@router.get("/aggregate", response_model=AggregatedReport)
def aggregate_expenses(
    session: SessionDep,
    current_user: CurrentUser,
    group_by: GroupBy = Query(...),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
) -> Any:
    filters = [Expense.user_id == current_user.id]

    if start_date:
        filters.append(Expense.date >= start_date)
    if end_date:
        filters.append(Expense.date < end_date + timedelta(days=1))

    if group_by == GroupBy.year:
        period_expr = func.date_trunc("year", Expense.date)
    elif group_by == GroupBy.month:
        period_expr = func.date_trunc("month", Expense.date)
    elif group_by == GroupBy.quarter:
        period_expr = func.date_trunc("quarter", Expense.date)

    stmt = (
        select(
            period_expr.label("period"),
            func.sum(Expense.amount).label("total_spent"),
            func.count().label("total_expenses"),
        )
        .where(*filters)
        .group_by(period_expr)
        .order_by(period_expr)
    )

    results = session.exec(stmt).all()

    aggregates: List[ExpenseAggregate] = [
        ExpenseAggregate(
            period=(
                row.period.strftime("%Y")
                if group_by == GroupBy.year
                else (
                    f"{row.period.year}-Q{(row.period.month - 1) // 3 + 1}"
                    if group_by == GroupBy.quarter
                    else row.period.strftime("%Y-%m")
                )
            ),
            total_spent=row.total_spent,
            total_expenses=row.total_expenses,
        )
        for row in results
    ]

    return AggregatedReport(
        user_id=current_user.id, group_by=group_by.value, aggregates=aggregates
    )
