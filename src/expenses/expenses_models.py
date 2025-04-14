from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel

from auth.auth_models import User, UserPublic
from categories.categories_models import Category


# base model
class ExpenseBase(SQLModel):
    date: datetime = Field(default_factory=datetime.now)
    amount: float = Field(..., gt=0)
    description: Optional[str] = None


# create model
class ExpenseCreate(ExpenseBase):
    user_id: int
    category_id: int


# update model
class ExpenseUpdate(ExpenseBase):
    pass


# API MODELS
class ExpensePublic(ExpenseBase):
    id: int
    user: UserPublic
    category: Category


class ExpensesPublic(SQLModel):
    data: list[ExpensePublic]
    count: int


# DATABASE MODELS
class Expense(ExpenseBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    category_id: int = Field(foreign_key="category.id")
    user: User = Relationship(back_populates="expenses")
    category: Category = Relationship(back_populates="expenses")
