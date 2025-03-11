import re
from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError, ConfigDict
from enum import Enum
from typing import Optional
from datetime import datetime, date

class UserType(str, Enum):
    client = "Клиент"
    business = "Бизнес"

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="Имя, от 1 до 50 символов")
    surname: Optional[str] = Field(None, min_length=1, max_length=50, description="Фамилия, от 1 до 50 символов")
    birthdate: Optional[date] = Field(None, description="Дата рождения в формате ГГГГ-ММ-ДД")
    mail: EmailStr = Field(None, description="Электронная почта")
    phone: Optional[str] = Field(None, description="Номер телефона в международном формате, начинающийся с '+'")
    
    model_config = ConfigDict(from_attributes=True)

    @field_validator("phone")
    @classmethod
    def validate_phone_number(cls, values: str) -> str:
        if values is not None and not re.match(r'^\+\d{1,15}$', values):
            raise ValueError('Номер телефона должен начинаться с "+" и содержать от 1 до 15 цифр')
        return values
    
    @field_validator("birthdate")
    @classmethod
    def validate_date_of_birth(cls, values: date) :
        if values and values >= datetime.now().date():
            raise ValueError('Дата рождения должна быть в прошлом')
        return values
    
class User(UserUpdate):    
    created_at: datetime
    updated_at: datetime

class UserLogin(BaseModel):
    login: str = Field(min_length=1, max_length=50, description="Login, от 1 до 50 символов")
    password: str = Field(min_length=1, max_length=50, description="Пароль, от 1 до 50 символов")

class UserRegistration(UserLogin):
    mail: EmailStr = Field(default=..., description="Электронная почта")

# Testig validating
def test_valid_user(data: dict) -> None:
    try:
        student = User(**data)
        print(student)
    except ValidationError as e:
        print(f"Ошибка валидации: {e}")
