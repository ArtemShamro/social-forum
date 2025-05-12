import pytest
import sys
from pathlib import Path
from conftest import RANDOM_STRINGS_GENERATE
from tests.unit.utils import generate_random_string
from app.api.crypt import get_password_hash, verify_password

RANDOM_STRINGS = [generate_random_string() for _ in range(RANDOM_STRINGS_GENERATE)]

@pytest.mark.parametrize("password", RANDOM_STRINGS)
def test_verify_password_correct(password):
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password) is True

@pytest.mark.parametrize("password", RANDOM_STRINGS)
def test_verify_password_incorrect(password):
    # Генерируем хэш для пароля
    hashed_password = get_password_hash(password)
    random_string = generate_random_string()
    assert verify_password(random_string, hashed_password) is False

def test_verify_password_empty():
    password = ""
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password) is True
    assert verify_password("notempty", hashed_password) is False
