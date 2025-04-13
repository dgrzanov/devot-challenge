from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from deps import CurrentUser, SessionDep
from categories.categories_models import (
    CategoriesPublic,
    Category,
    CategoryCreate,
    CategoryPublic,
    CategoryUpdate,
)

router = APIRouter(tags=["categories"])


@router.get("/", response_model=CategoriesPublic)
def get_all_categories(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Get categories.
    """

    count_statement = select(func.count()).select_from(Category)
    count = session.exec(count_statement).one()
    statement = select(Category).offset(skip).limit(limit)
    categories = session.exec(statement).all()

    return CategoriesPublic(data=categories, count=count)


@router.get("/{id}", response_model=CategoryPublic)
def get_single_category(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Get category by ID.
    """
    category = session.get(Category, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryPublic)
def create_category(
    *, session: SessionDep, current_user: CurrentUser, category_in: CategoryCreate
) -> Any:
    """
    Create new category.
    """
    category = Category.model_validate(category_in)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.put("/{id}", response_model=CategoryPublic)
def update_category(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: int,
    category_in: CategoryUpdate,
) -> Any:
    """
    Update a category.
    """
    category = session.get(Category, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    update_dict = category_in.model_dump(exclude_unset=True)
    category.sqlmodel_update(update_dict)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.delete("/{id}")
def delete_category(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Delete a category.
    """
    category = session.get(Category, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(category)
    session.commit()
    return {"message": "Category deleted successfully"}
