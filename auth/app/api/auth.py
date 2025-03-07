from fastapi import APIRouter, HTTPException, Response, status, Depends,Request
from app.api.crypt import get_password_hash
from app.api.db_manager import UserDB
from app.api import models
import app.api.crypt as crypt
from app.api.models import User

auth = APIRouter()

@auth.get('/all')
async def register():
    print("GET ALL USERS")
    users = await UserDB.get_all_users()
    return users



@auth.get("/me")
async def get_me(user_data = Depends(crypt.get_current_user)):
    user_data = User.model_validate(user_data)
    return user_data.model_dump()

@auth.post('/register')
async def register(payload: models.UserRegistration):

    user = await UserDB.find_one_or_none_by_login(payload.login)
    if user:
        raise HTTPException(status_code=400, detail="User already registered!")
    
    payload.password = crypt.get_password_hash(payload.password)
    await UserDB.add_user(payload)
    
    response = {
        "messege" : "Success!"
    }
    return response

@auth.post('/update')
async def update(request: Request):
    try:
        user_token = crypt.get_token(request)
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not login!')
    
    user = await crypt.get_current_user(user_token)
    payload = await request.json()
    
    await UserDB.update_user(payload, user.id)
    
    response = {
        "messege" : "Success!"
    }
    
    return response

@auth.post("/login")
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

