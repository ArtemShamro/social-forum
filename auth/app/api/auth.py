from fastapi import APIRouter, Response, status, Depends,Request
from fastapi.exceptions import HTTPException
from app.api.crypt import get_password_hash
from app.api.db_manager import UserDB
from app.api import schemas
import app.api.crypt as crypt
from app.api.schemas import User, UserUpdate
from typing import List
from app.api.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

auth = APIRouter()

@auth.get('/all', response_model=List[User], summary="Получить список всех пользователей")
async def register():
    print("GET ALL USERS")
    users = await UserDB.get_all_users()
    return users


@auth.get("/me", response_model=User, summary="Получить информацию текущего пользователя", 
          responses={
    401: {"description": "Вход не выполнен"}
})
async def get_me(user_id = Depends(crypt.get_current_user), session: AsyncSession = Depends(get_db)):
    
    user = await UserDB.find_one_or_none_by_id(user_id, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    
    user_data = User.model_validate(user)
    
    return user_data

@auth.post('/register', summary="Регистрация", responses={
        400: {"description": "Логин занят"},
        422: {"description": "Ошибка валидации"}
}) 
async def register(payload: schemas.UserRegistration, session: AsyncSession = Depends(get_db)):
    print(payload.login)
    user = await UserDB.find_one_or_none_by_login(payload.login, session)
    if user:
        raise HTTPException(status_code=400, detail="Логин занят!")
    
    payload.password = crypt.get_password_hash(payload.password)
    await UserDB.add_user(payload, session)
    
    response = {
        "messege" : "Success!"
    }
    return response

@auth.post('/update', summary="Обновить информацию текущего пользователя", responses={
        401: {"description": "Вход не выполнен"},
        422: {"description": "Ошибка валидации"}
})
async def update(request: Request, payload: UserUpdate, session: AsyncSession = Depends(get_db)):
    
    user_token = crypt.get_token(request)
    user_id = await crypt.get_current_user(user_token)
    
    await UserDB.update_user(payload, user_id, session)
    
    response = {
        "messege" : "Success!"
    }
    
    return response

@auth.post("/login", summary="Login", responses={
        401: {"description": "Пользователь не найден"},
        422: {"description": "Ошибка валидации"}
})
async def auth_user(response: Response, user_data: schemas.UserLogin, session: AsyncSession = Depends(get_db)):
    check = await authenticate_user(user_data.login, user_data.password, session)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = crypt.create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}


async def authenticate_user(login: str, password: str, session: AsyncSession):
    user = await UserDB.find_one_or_none_by_login(login, session)
    if not user or crypt.verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user

