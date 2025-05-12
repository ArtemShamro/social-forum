import pytest
import sys
from pathlib import Path
from tests.unit.utils import generate_random_string
from tests.unit.crypto.conftest import RANDOM_STRINGS_GENERATE

from app.api.crypt import get_password_hash
RANDOM_STRINGS = [generate_random_string() for _ in range(RANDOM_STRINGS_GENERATE)]

@pytest.mark.parametrize("password", RANDOM_STRINGS)
def test_get_password_hash_returns_string(password):
    hashed_password = get_password_hash(password)
    assert isinstance(hashed_password, str)

@pytest.mark.parametrize("password", RANDOM_STRINGS)
def test_get_password_hash_not_equal_to_original(password):
    hashed_password = get_password_hash(password)
    assert hashed_password != password

@pytest.mark.parametrize("password", RANDOM_STRINGS)
def test_get_password_hash_different_for_same_password(password):
    hashed_password1 = get_password_hash(password)
    hashed_password2 = get_password_hash(password)
    assert hashed_password1 != hashed_password2

def test_get_password_hash_with_empty_string():
    password = ""
    hashed_password = get_password_hash(password)
    assert isinstance(hashed_password, str)
    assert hashed_password != password

@pytest.mark.parametrize("password", RANDOM_STRINGS)
def test_get_password_hash_length(password):
    hashed_password = get_password_hash(password)
    assert len(hashed_password) == 60

@pytest.mark.parametrize("password", RANDOM_STRINGS)
def test_get_password_hash_unique(password):
    hashed_password = get_password_hash(password)
    random_string = generate_random_string()
    random_hash = get_password_hash(random_string)
    assert hashed_password != random_hash