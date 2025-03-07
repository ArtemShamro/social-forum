from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.auth import auth
from app.api.db import init_db, engine

# metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan, openapi_url="/api/v1/auth/openapi.json", docs_url="/api/v1/auth/docs")

# app.include_router(auth)

app.include_router(auth) # prefix='/api/v1/auth', tags=['auth']
