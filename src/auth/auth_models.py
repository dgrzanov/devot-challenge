from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    full_name: str | None = Field(default=None, max_length=255)
    balance: float = Field(default=1000.0)  # for simplicity predefined


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserRegister(SQLModel):
    username: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


class UserPublic(UserBase):
    id: int


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None


# DATABASE MODELS
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    expenses: list["Expense"] = Relationship(back_populates="user")
