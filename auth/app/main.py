from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.api.auth import auth
from app.api.db import init_db

# metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan, openapi_url="/api/v1/auth/openapi.json", docs_url="/api/v1/auth/docs")

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 401 and exc.detail == 'Token not found':
        return JSONResponse(
            status_code=401,
            content={"message": "Необходимо зайдти или зарегистрироваться!"},
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

app.include_router(auth) # prefix='/api/v1/auth', tags=['auth']
