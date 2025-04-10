from sqlmodel import Field, Relationship, SQLModel


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    full_name: str | None = Field(default=None, max_length=255)
    balance: float = Field(default=1000.0)  # for simplicity predefined


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None


# DATABASE MODELS
class User(UserBase, table=True):
    id: int = Field(primary_key=True)
    hashed_password: str
