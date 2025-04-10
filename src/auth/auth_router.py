from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi import security
from fastapi.security import OAuth2PasswordRequestForm

from auth.auth_models import Token
from config import settings
from core import auth
from deps import CurrentUser, SessionDep


router = APIRouter(tags=["auth"])


@router.get("/")
async def test(session: SessionDep, current_user: CurrentUser):
    return {"message": "Authenticated!", "user": current_user}


@router.post("/login")
def login(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = auth.authenticate(
        session=session, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )
