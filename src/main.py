from fastapi import FastAPI, APIRouter

from config import settings

from auth.auth_router import router as auth_router
from categories.categories_router import router as categories_router

app = FastAPI()

app.include_router(auth_router, prefix=settings.ROOT_URL + "/auth")
app.include_router(categories_router, prefix=settings.ROOT_URL + "/categories")
