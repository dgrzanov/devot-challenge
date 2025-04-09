from fastapi import FastAPI, APIRouter

import config

from auth.auth_router import router as auth_router

app = FastAPI()

app.include_router(auth_router, prefix=config.ROOT_URL + "/auth")
