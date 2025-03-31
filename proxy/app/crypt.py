from passlib.context import CryptContext
from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from app.config import Config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Token not found')
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        auth_data = Config.ENC_DATA
        payload = jwt.decode(token, auth_data['secret_key'], 
                             algorithms=[auth_data['algorithm']])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Токен не валидный!')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        return -1
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail='Не найден ID пользователя')

    return user_id