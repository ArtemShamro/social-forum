import pytest
from datetime import datetime, date, timedelta
from pydantic import ValidationError
from app.api.schemas import UserUpdate, User, UserLogin, UserRegistration  # 

# Тесты для модели UserUpdate
def test_user_update_valid_data():
    # Корректные данные
    data = {
        "name": "Иван",
        "surname": "Иванов",
        "birthdate": date(1990, 1, 1),
        "mail": "ivan@example.com",
        "phone": "+79123456789"
    }
    user = UserUpdate(**data)
    assert user.name == "Иван"
    assert user.surname == "Иванов"
    assert user.birthdate == date(1990, 1, 1)
    assert user.mail == "ivan@example.com"
    assert user.phone == "+79123456789"

def test_user_update_invalid_name():
    # Некорректное имя (пустая строка)
    with pytest.raises(ValidationError):
        UserUpdate(name="", surname="Иванов")

def test_user_update_invalid_surname():
    # Некорректная фамилия (слишком длинная)
    with pytest.raises(ValidationError):
        UserUpdate(name="Иван", surname="A" * 51)

def test_user_update_invalid_birthdate():
    # Некорректная дата рождения (в будущем)
    future_date = datetime.now().date() + timedelta(days=1)
    with pytest.raises(ValidationError):
        UserUpdate(name="Иван", surname="Иванов", birthdate=future_date)

def test_user_update_invalid_email():
    # Некорректный email
    with pytest.raises(ValidationError):
        UserUpdate(name="Иван", surname="Иванов", mail="invalid-email")

def test_user_update_invalid_phone():
    # Некорректный номер телефона
    with pytest.raises(ValidationError):
        UserUpdate(name="Иван", surname="Иванов", phone="89123456789")  # Нет "+"

# Тесты для модели UserLogin
def test_user_login_valid_data():
    # Корректные данные
    data = {
        "login": "user123",
        "password": "password123"
    }
    user = UserLogin(**data)
    assert user.login == "user123"
    assert user.password == "password123"

def test_user_login_invalid_login():
    # Некорректный логин (пустая строка)
    with pytest.raises(ValidationError):
        UserLogin(login="", password="password123")

def test_user_login_invalid_password():
    # Некорректный пароль (слишком длинный)
    with pytest.raises(ValidationError):
        UserLogin(login="user123", password="A" * 51)

# Тесты для модели UserRegistration
def test_user_registration_valid_data():
    # Корректные данные
    data = {
        "login": "user123",
        "password": "password123",
        "mail": "user@example.com"
    }
    user = UserRegistration(**data)
    assert user.login == "user123"
    assert user.password == "password123"
    assert user.mail == "user@example.com"

def test_user_registration_invalid_email():
    # Некорректный email
    with pytest.raises(ValidationError):
        UserRegistration(login="user123", password="password123", mail="invalid-email")

# Тесты для модели User
def test_user_valid_data():
    # Корректные данные
    data = {
        "name": "Иван",
        "surname": "Иванов",
        "birthdate": date(1990, 1, 1),
        "mail": "ivan@example.com",
        "phone": "+79123456789",
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    user = User(**data)
    assert user.name == "Иван"
    assert user.surname == "Иванов"
    assert user.birthdate == date(1990, 1, 1)
    assert user.mail == "ivan@example.com"
    assert user.phone == "+79123456789"

def test_user_missing_required_fields():
    # Отсутствие обязательных полей
    with pytest.raises(ValidationError):
        User(name="Иван", surname="Иванов")  # Пропущены created_at и updated_at