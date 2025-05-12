import httpx
from app.models.user import UserCreate, generate_random_user
from app.core.config import MAIN_APP_API_URL
from typing import Optional
from app.utils.user_store import save_user


def register_user(user: UserCreate):
    url = f"{MAIN_APP_API_URL}/auth/register"
    data = {
        "login": user.login,
        "password": user.password,
        "mail": user.mail
    }
    try:
        response = httpx.post(url, json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        print(f"Registration failed: {exc.response.status_code} - {exc.response.text}")
        return None
    except Exception as exc:
        print(f"Registration error: {exc}")
        return None


def login_user(user: UserCreate):
    url = f"{MAIN_APP_API_URL}/auth/login"
    data = {
        "login": user.login,
        "password": user.password
    }
    try:
        response = httpx.post(url, json=data, timeout=10)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        print(f"Login failed: {exc.response.status_code} - {exc.response.text}")
        return None
    except Exception as exc:
        print(f"Login error: {exc}")
        return None


def update_user_profile(user: UserCreate, token: Optional[str] = None):
    url = f"{MAIN_APP_API_URL}/auth/update"
    cookies = {}
    if token:
        cookies["users_access_token"] = token
    data = {
        "name": user.name,
        "surname": user.surname,
        "birthdate": user.birthdate.isoformat() if user.birthdate else None,
        "mail": user.mail,
        "phone": user.phone
    }
    try:
        response = httpx.post(url, json=data, cookies=cookies, timeout=10)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        print(f"Profile update failed: {exc.response.status_code} - {exc.response.text}")
        return None
    except Exception as exc:
        print(f"Profile update error: {exc}")
        return None


if __name__ == "__main__":
    user = generate_random_user()
    print("Registering user:", user.login)
    reg_result = register_user(user)
    print("Registration result:", reg_result)
    if reg_result:
        save_user(user)
        print(f"User {user.login} saved to user store.")
        print("Logging in user...")
        login_result = login_user(user)
        print("Login result:", login_result)
        token = None
        if login_result:
            token = login_result.get('user_access_token') or login_result.get('access_token')
        print("Updating profile...")
        upd_result = update_user_profile(user, token=token)
        print("Profile update result:", upd_result)
    else:
        print("Registration failed, skipping login and profile update.")
