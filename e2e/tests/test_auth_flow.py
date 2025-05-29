import pytest
import httpx

@pytest.mark.asyncio
async def test_full_auth_flow():
    async with httpx.AsyncClient() as client:
        # Регистрация
        reg_response = await client.post(
            "http://proxy:8000/register",
            json={"login": "test_user", "password": "strongpass"}
        )
        assert reg_response.status_code == 200

        # Логин
        login_response = await client.post(
            "http://proxy:8000/login",
            json={"login": "test_user", "password": "strongpass"}
        )
        assert login_response.status_code == 200
        assert "access_token" in login_response.json()

        # Проверка текущего пользователя
        headers = {"Cookie": f"users_access_token={login_response.json()['access_token']}"}
        me_response = await client.get(
            "http://proxy:8000/me",
            headers=headers
        )
        assert me_response.status_code == 200
        assert me_response.json()["login"] == "test_user"
