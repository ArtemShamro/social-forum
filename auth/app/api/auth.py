from fastapi import APIRouter, Response, status, Depends,Request
from fastapi.exceptions import HTTPException
from app.api.crypt import get_password_hash
from app.api.db_manager import UserDB
from app.api import models
import app.api.crypt as crypt
from app.api.models import User, UserUpdate
from typing import List
from fastapi.responses import JSONResponse

auth = APIRouter()

@auth.get('/all', response_model=List[User], summary="Получить список всех пользователей")
async def register():
    print("GET ALL USERS")
    users = await UserDB.get_all_users()
    return users


@auth.get("/me", response_model=User, summary="Получить информацию текущего пользователя", responses={
    401: {"description": "Вход не выполнен"}
})
async def get_me(user_data = Depends(crypt.get_current_user)):
    
    user_data = User.model_validate(user_data)
    
    return user_data

@auth.post('/register', summary="Регистрация", responses={
        400: {"description": "Логин занят"},
        422: {"description": "Ошибка валидации"}
}) 
async def register(payload: models.UserRegistration):

    user = await UserDB.find_one_or_none_by_login(payload.login)
    if user:
        raise HTTPException(status_code=400, detail="Логин занят!")
    
    payload.password = crypt.get_password_hash(payload.password)
    await UserDB.add_user(payload)
    
    response = {
        "messege" : "Success!"
    }
    return response

@auth.post('/update', summary="Обновить информацию текущего пользователя", responses={
        401: {"description": "Вход не выполнен"},
        422: {"description": "Ошибка валидации"}
})
async def update(request: Request, payload: UserUpdate):
    
    user_token = crypt.get_token(request)
    user = await crypt.get_current_user(user_token)
    
    await UserDB.update_user(payload, user.id)
    
    response = {
        "messege" : "Success!"
    }
    
    return response

@auth.post("/login", summary="Login", responses={
        401: {"description": "Пользователь не найден"},
        422: {"description": "Ошибка валидации"}
})
async def auth_user(response: Response, user_data: models.UserLogin):
    check = await authenticate_user(user_data.login, user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = crypt.create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}

async def authenticate_user(login: str, password: str):
    user = await UserDB.find_one_or_none_by_login(login)
    if not user or crypt.verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user

