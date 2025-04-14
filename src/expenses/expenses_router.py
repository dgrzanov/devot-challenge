from datetime import date
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import func, select

from deps import CurrentUser, SessionDep
from expenses.expenses_dal import update_user_balance
from expenses.expenses_models import (
    ExpensesPublic,
    Expense,
    ExpenseCreate,
    ExpensePublic,
    ExpenseUpdate,
)

router = APIRouter(tags=["expenses"])


@router.get("/", response_model=ExpensesPublic)
def get_all_expenses(
    session: SessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
    category: Optional[int] = Query(None),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
) -> Any:
    """
    Get expenses.
    """

    filters = [Expense.user_id == current_user.id]

    if category:
        filters.append(Expense.category_id == category)
    if min_amount:
        filters.append(Expense.amount >= min_amount)
    if max_amount:
        filters.append(Expense.amount <= max_amount)
    if start_date:
        filters.append(Expense.date >= start_date)
    if end_date:
        filters.append(Expense.date <= end_date)

    count_statement = select(func.count()).select_from(Expense).where(*filters)
    count = session.exec(count_statement).one()
    statement = select(Expense).where(*filters).offset(skip).limit(limit)
    expenses = session.exec(statement).all()

    return ExpensesPublic(data=expenses, count=count)


@router.get("/{id}", response_model=ExpensePublic)
def get_single_expense(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Get expense by ID.
    """
    expense = session.get(Expense, id)
    if expense.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not allowed to access this expense"
        )
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.post("/", response_model=ExpensePublic)
def create_expense(
    *, session: SessionDep, current_user: CurrentUser, expense_in: ExpenseCreate
) -> Any:
    """
    Create new expense.
    """
    expense = Expense.model_validate(expense_in)
    expense.user_id = current_user.id
    session.add(expense)
    session.commit()
    update_user_balance(session, current_user.id, expense.amount)
    session.refresh(expense)

    return expense


@router.put("/{id}", response_model=ExpensePublic)
def update_expense(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: int,
    expense_in: ExpenseUpdate,
) -> Any:
    """
    Update a expense.
    """
    expense = session.get(Expense, id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    if expense.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You are not allowed to access this expense"
        )
    difference = expense_in.amount - expense.amount
    update_dict = expense_in.model_dump(exclude_unset=True)
    expense.sqlmodel_update(update_dict)
    session.add(expense)
    session.commit()
    if difference != 0:
        update_user_balance(session, current_user.id, difference)
    session.refresh(expense)

    return expense


@router.delete("/{id}")
def delete_expense(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Delete a expense.
    """
    expense = session.get(Expense, id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    session.delete(expense)
    session.commit()

    update_user_balance(session, current_user.id, -expense.amount)

    return {"message": "Expense deleted successfully"}
