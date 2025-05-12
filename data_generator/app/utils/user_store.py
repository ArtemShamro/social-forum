import os
import json
from app.models.user import UserCreate
from typing import List

USER_STORE_PATH = "data_generator/users.json"


def save_user(user: UserCreate):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(USER_STORE_PATH), exist_ok=True)
    try:
        users = load_users()
    except Exception:
        users = []
    # Always convert all users to dicts before saving
    users_dicts = [u.model_dump(mode="json") if isinstance(u, UserCreate) else u for u in users]
    users_dicts.append(user.model_dump(mode="json"))
    with open(USER_STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(users_dicts, f, ensure_ascii=False, indent=2)


def load_users() -> List[UserCreate]:
    if not os.path.exists(USER_STORE_PATH) or os.path.getsize(USER_STORE_PATH) == 0:
        return []
    with open(USER_STORE_PATH, "r", encoding="utf-8") as f:
        users_data = json.load(f)
    return [UserCreate(**u) for u in users_data]
