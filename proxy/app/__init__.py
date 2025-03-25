from fastapi import FastAPI

def init_app(init_db=True):

    app = FastAPI(openapi_url="/api/v1/proxy/openapi.json", docs_url="/api/v1/proxy/docs")
    
    from app.proxy_auth import auth
    from app.proxy_posts import posts

    app.include_router(auth, prefix='/auth') # prefix='/api/v1/auth', tags=['auth']
    app.include_router(posts, prefix="/posts") # prefix='/api/v1/auth', tags=['auth']


    return app