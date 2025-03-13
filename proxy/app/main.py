from fastapi import FastAPI, Request, Response
import httpx

app = FastAPI()
BACKEND_URL = "http://auth:8000"  # Адрес основного сервиса


@app.post("/login")
async def auth_user(response: Response, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{BACKEND_URL}/login"
        headers = dict(request.headers)
        print(headers)

        content = await request.body()
        content_json = await request.json()

        request_params = {
            "method": "POST",
            "url": url,
            "headers": headers
        }

        if content:
            request_params["json"] = content_json
            request_params["headers"].pop("content-length", None)

        response_backend = await client.request(**request_params)
        access_token = response_backend.json().get("access_token")
        response.set_cookie(key="users_access_token", value=access_token, httponly=True)

        print(response)
        
    return {'access_token': access_token, 'refresh_token': None}

@app.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        method = request.method
        url = f"{BACKEND_URL}/{path}"
        headers = dict(request.headers)
        content = await request.body()
        request_params = {
            "method": method,
            "url": url,
            "headers": headers
        }

        if content:
            content_json = await request.json()
            request_params["json"] = content_json
            request_params["headers"].pop("content-length", None)

        response = await client.request(**request_params)
        
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )