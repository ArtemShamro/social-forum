from fastapi import FastAPI

from app.api.config import Config

def init_app(init_db=True):
    lifespan = None

    if init_db:
        print("APP: INIT DB")
        from app.api.db import sessionmanager

        sessionmanager.init(Config.DB_CONFIG)

    app = FastAPI(lifespan=lifespan, openapi_url="/api/v1/auth/openapi.json", docs_url="/api/v1/auth/docs")
    
    from app.api.auth import auth

    app.include_router(auth) # prefix='/api/v1/auth', tags=['auth']

    return app