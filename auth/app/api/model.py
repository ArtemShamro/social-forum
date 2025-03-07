from pydantic import BaseModel
from typing import List
from datetime import datetime, date

class User(BaseModel):
    name: str
    surname: str
    birthdate: date
    mail: str
    phone: str
    created_at: datetime
    updated_at: datetime

class UserLogin(BaseModel):
    login: str
    password: str

class UserRegistration(UserLogin):
    mail: str
