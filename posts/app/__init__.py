from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio


from app.api.posts import serve
from app.api.config import Config

def init_app(init_db=True):

    if init_db:
        print("APP: INIT DB")
        from app.api.db import sessionmanager

        sessionmanager.init(Config.DB_CONFIG)

    from app.api.posts import serve

    
    app = FastAPI(lifespan=serve, openapi_url="/api/v1/auth/openapi.json", docs_url="/api/v1/auth/docs")
    
    return app