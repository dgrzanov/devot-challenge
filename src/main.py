from fastapi import FastAPI, APIRouter

from config import settings

from auth.auth_router import router as auth_router
from categories.categories_router import router as categories_router
from expenses.expenses_router import router as expenses_router
from report.report_router import router as report_router

tags_metadata = [
    {
        "name": "auth",
        "description": "Endpoints related to authentication.",
    },
    {
        "name": "categories",
        "description": "Endpoints related to categories.",
    },
    {
        "name": "expenses",
        "description": "Endpoints related to expenses.",
    },
    {
        "name": "report",
        "description": "Endpoints related to reports.",
    },
]

app = FastAPI(
    title="Devot Challenge",
    description="API for Devot Challenge",
    version="0.0.1",
    contact={
        "name": "Dino Gržanov",
        "email": "dino.grzanov@gmail.com",
    },
    openapi_tags=tags_metadata,
)

app.include_router(auth_router, prefix=settings.ROOT_URL + "/auth")
app.include_router(categories_router, prefix=settings.ROOT_URL + "/categories")
app.include_router(expenses_router, prefix=settings.ROOT_URL + "/expenses")
app.include_router(report_router, prefix=settings.ROOT_URL + "/report")
