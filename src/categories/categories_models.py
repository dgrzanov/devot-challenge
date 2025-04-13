from typing import Optional
from sqlmodel import Field, SQLModel


# base model
class CategoryBase(SQLModel):
    name: str = Field(index=True, unique=True)


# create model
class CategoryCreate(CategoryBase):
    pass


# update model
class CategoryUpdate(CategoryBase):
    pass


# API MODELS
class CategoryPublic(CategoryBase):
    id: int
    name: str


class CategoriesPublic(SQLModel):
    data: list[CategoryPublic]
    count: int


# DATABASE MODELS
class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
