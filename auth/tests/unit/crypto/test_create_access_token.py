import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.api.crypt import create_access_token
from app.api.config import Config
# from app import

def test_create_access_token_returns_string():
    data = {"sub": "user123"}
    token = create_access_token(data)
    assert isinstance(token, str)

def test_create_access_token_contains_data():
    expire_datetime = datetime.now(timezone.utc)
    data = {"sub": "user123", "exp": expire_datetime}
    token = create_access_token(data)
    decoded_data = jwt.decode(token, Config.ENC_DATA['secret_key'], algorithms=[Config.ENC_DATA['algorithm']])
    assert decoded_data["sub"] == "user123"

    expire_timestamp = decoded_data["exp"]
    expire_datetime = datetime.fromtimestamp(expire_timestamp, timezone.utc)
    assert abs((expire_datetime - expire_datetime).total_seconds()) < 1