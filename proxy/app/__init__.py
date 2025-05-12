from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def init_app(init_db=True):

    app = FastAPI(openapi_url="/api/v1/proxy/openapi.json",
                  docs_url="/api/v1/proxy/docs")

    origins = [
        "http://localhost.tiangolo.com",
        "https://localhost.tiangolo.com",
        "http://localhost",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.proxy_auth import auth
    from app.proxy_posts import posts
    from app.proxy_utils import utils
    from app.proxy_stats import stats

    # prefix='/api/v1/auth', tags=['auth']
    app.include_router(auth, prefix='/auth')
    # prefix='/api/v1/auth', tags=['auth']
    app.include_router(posts, prefix="/posts")
    app.include_router(utils, prefix="/utils")
    app.include_router(stats, prefix="/stats")

    return app
