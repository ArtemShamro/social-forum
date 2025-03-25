import re
from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError, ConfigDict
from enum import Enum
from typing import Optional
from datetime import datetime, date

class PostCreate(BaseModel):
    owner_id: Optional[str] = Field(None, min_length=1, max_length=50, description="Имя, от 1 до 50 символов")
    title: Optional[str] = Field(None, min_length=1, max_length=10000, description="Описание, от 1 до 10000 символов")
    description: Optional[str] = Field(None, min_length=1, max_length=50, description="Фамилия, от 1 до 50 символов")
    private: Optional[bool] = Field(False, description="Приватность поста")
    
    model_config = ConfigDict(from_attributes=True)
    
class BasicResponce(BaseModel):    
    status_code: datetime
    message: datetime

# class UserLogin(BaseModel):
#     login: str = Field(min_length=1, max_length=50, description="Login, от 1 до 50 символов")
#     password: str = Field(min_length=1, max_length=50, description="Пароль, от 1 до 50 символов")

# class UserRegistration(UserLogin):
#     mail: EmailStr = Field(default=..., description="Электронная почта")

# # Testig validating
# def test_valid_user(data: dict) -> None:
#     try:
#         student = User(**data)
#         print(student)
#     except ValidationError as e:
#         print(f"Ошибка валидации: {e}")
