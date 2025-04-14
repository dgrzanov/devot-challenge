from datetime import datetime
from enum import Enum
from typing import List
from sqlmodel import Field, SQLModel


class ReportByPeriod(SQLModel):
    total_spent: float
    total_expenses: int
    average_spent: float
    start_date: datetime
    end_date: datetime
    user_id: int = Field(foreign_key="user.id")
    spent_by_category: dict[str, float] = Field(default={})


class GroupBy(str, Enum):
    year = "year"
    quarter = "quarter"
    month = "month"


class ExpenseAggregate(SQLModel):
    period: str
    total_spent: float
    total_expenses: int


class AggregatedReport(SQLModel):
    user_id: int
    group_by: str
    aggregates: List[ExpenseAggregate]
