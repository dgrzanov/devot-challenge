from collections.abc import Generator
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from auth.auth_models import TokenPayload, User
from core.db import engine
from config import settings

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.ROOT_URL}/auth/login")


def get_db() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session for each request.
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
