from fastapi import Request
from app.crypt import get_token, get_current_user

async def check_login(request):
    access_token = get_token(request)
    user_id = await get_current_user(access_token)
    return user_id


async def check_login_or_zero(request):
    try:
        access_token = get_token(request)
        user_id = await get_current_user(access_token)
    except:
        user_id = "0"
    return user_id


def grpc_post_responce_to_json(response):
    return {
        "post_id": response.post_id,
        "owner_id": response.owner_id,
        "title": response.title,
        "description": response.description,
        "private": response.private,
        "created_at": response.created_at,
        "updated_at": response.updated_at
    }