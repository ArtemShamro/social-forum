from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio
from contextlib import asynccontextmanager

from app.api.posts import serve
from app.api.config import Config

def init_app(init_db=True):

    if init_db:
        print("APP: INIT DB")
        from app.api.db import sessionmanager

        sessionmanager.init(Config.DB_CONFIG)

    from app.api.posts import serve

    # @asynccontextmanager
    # async def lifespan(app):
    #     loop = asyncio.get_event_loop()
    #     loop.run_in_executor(None, serve, app)
    #     yield
    #     if hasattr(app.state, 'grpc_server'):
    #         app.state.grpc_server.stop(grace=2)
    
    app = FastAPI(lifespan=serve, openapi_url="/api/v1/auth/openapi.json", docs_url="/api/v1/auth/docs")
    
    return app


