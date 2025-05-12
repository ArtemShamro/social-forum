from fastapi import Request, Response, APIRouter
import httpx

from app.schemas import *

from app.config import Config
from app.kafka_producer import KafkaProducer
BACKEND_URL = Config.AUTH_URL


auth = APIRouter()
kafka_producer = KafkaProducer()


@auth.post("/register")
async def register_user(request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{BACKEND_URL}/register"
        headers = dict(request.headers)
        content = await request.body()
        request_params = {
            "method": "POST",
            "url": url,
            "headers": headers,
            "content": content
        }
        try:
            response = await client.request(**request_params)
            print(response.json())
            if response.status_code == 200:
                kafka_producer.send_user_registration_event(
                    user_data=response.json()['user'])
        except httpx.HTTPError as exc:
            return exc.response.json()
    return response.json()


@auth.post("/login")
async def auth_user(response: Response, request: Request):
    print("REQUEST:", request)
    async with httpx.AsyncClient() as client:
        url = f"{BACKEND_URL}/login"
        headers = dict(request.headers)

        content = await request.body()
        content_json = await request.json()

        print(content_json)

        request_params = {
            "method": "POST",
            "url": url,
            "headers": headers
        }

        if content:
            request_params["json"] = content_json
            request_params["headers"].pop("content-length", None)

        response_backend = await client.request(**request_params)
        print(response_backend.json())
        access_token = response_backend.json().get("user_access_token")
        response.set_cookie(key="users_access_token",
                            value=access_token, httponly=True,
                            samesite="Lax", secure=False)

    return {'access_token': access_token, 'refresh_token': None}


@auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}


@auth.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
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
