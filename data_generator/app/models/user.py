# Placeholder for user data models

from pydantic import BaseModel, EmailStr
from typing import Optional
from faker import Faker
import random
import string
from datetime import date


class UserCreate(BaseModel):
    login: str
    password: str
    name: Optional[str] = None
    surname: Optional[str] = None
    birthdate: Optional[date] = None
    mail: EmailStr
    phone: Optional[str] = None
    is_user: bool = True
    is_business: bool = False


fake = Faker()


def generate_random_user():
    login = fake.user_name()
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    name = fake.first_name()
    surname = fake.last_name()
    birthdate = fake.date_of_birth(minimum_age=18, maximum_age=80)
    mail = fake.email()
    phone = f"+{fake.random_number(digits=10, fix_len=True)}"
    return UserCreate(
        login=login,
        password=password,
        name=name,
        surname=surname,
        birthdate=birthdate,
        mail=mail,
        phone=phone,
        is_user=True,
        is_business=False
    )


if __name__ == "__main__":
    user = generate_random_user()
    import json
    print(json.dumps(user.model_dump(), indent=2, ensure_ascii=False))
