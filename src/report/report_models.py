from datetime import datetime
from sqlmodel import Field, SQLModel


# base model
class ReportByPeriod(SQLModel):
    total_spent: float
    total_expenses: int
    average_spent: float
    start_date: datetime
    end_date: datetime
    user_id: int = Field(foreign_key="user.id")
    spent_by_category: dict[str, float] = Field(default={})
