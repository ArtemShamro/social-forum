from app.api.schemas import UserRegistration
from app.api.db_manager import UserDB
from app.api.db import get_db
import pytest 

@pytest.mark.asyncio
async def test_register_user(client, session):
    payload = {
        "login": "testuser",
        "password": "testpassword",
        "mail": "test@example.com"
    }

    response = client.post("/register", json=payload)
    assert response.status_code == 200
    assert response.json() == {"messege": "Success!"}

    # Проверяем, что пользователь добавлен в базу данных
    user = await UserDB.find_one_or_none_by_login("testuser", session)
    assert user is not None
    assert user.mail == "test@example.com"

@pytest.mark.asyncio
async def test_get_me(client, session):
    # Сначала регистрируем пользователя
    payload = {
        "login": "testuser",
        "password": "testpassword",
        "mail": "test@example.com"
    }
    client.post("/register", json=payload)

    # Логинимся, чтобы получить токен
    login_payload = {
        "login": "testuser",
        "password": "testpassword"
    }
    login_response = client.post("/login", json=login_payload)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    # Получаем информацию о текущем пользователе
    client.cookies = {"users_access_token": access_token}
    response = client.get("/me")
    assert response.status_code == 200
    assert response.json()["mail"] == "test@example.com"

@pytest.mark.asyncio
async def test_update_user(client, session):
    # Сначала регистрируем пользователя
    payload = {
        "login": "testuser",
        "password": "testpassword",
        "mail": "test@example.com"
    }
    client.post("/register", json=payload)

    # Логинимся, чтобы получить токен
    login_payload = {
        "login": "testuser",
        "password": "testpassword"
    }
    login_response = client.post("/login", json=login_payload)
    access_token = login_response.json()["access_token"]

    # Обновляем информацию пользователя
    update_payload = {
        "name": "New Name",
        "surname": "New Surname",
        "birthdate": "2000-01-01",
        "mail": "name1@mail.ru",
        "phone": "+01234567890"
    }

    client.cookies = {"users_access_token": access_token}
    response = client.post("/update", json=update_payload)
    assert response.status_code == 200
    assert response.json() == {"messege": "Success!"}

    # Проверяем, что информация обновлена в базе данных
    user = await UserDB.find_one_or_none_by_login("testuser", session)
    assert user.name == "New Name"
    assert user.surname == "New Surname"
    assert user.birthdate.isoformat() == "2000-01-01"
    assert user.mail == "name1@mail.ru"
    assert user.phone == "+01234567890"