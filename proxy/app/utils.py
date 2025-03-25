from fastapi import Request
from app.crypt import get_token, get_current_user

async def check_login(request):
    access_token = get_token(request)
    user_id = await get_current_user(access_token)
    return user_id
