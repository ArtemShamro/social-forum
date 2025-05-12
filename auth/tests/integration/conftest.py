import asyncio
from contextlib import ExitStack

import pytest
import pytest_asyncio

from fastapi.testclient import TestClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor

import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(root_dir))

from app import init_app
from app.api.db import sessionmanager, get_db

# Фикстура для инициализации тестовой базы данных
test_db = factories.postgresql_proc(port=None, dbname="test_db")

@pytest_asyncio.fixture(scope="session", autouse=True)
async def connection_test(test_db):
    print("CONNECTION TEST")
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor(
        user=pg_user,
        host=pg_host,
        port=pg_port,
        dbname=pg_db,
        version=test_db.version,
        password=pg_password
    ):
        connection_str = f"postgresql+psycopg://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
        sessionmanager.init(connection_str)
        yield
        await sessionmanager.close()

@pytest.fixture(autouse=True)
def app(connection_test):
    print("EDIT STACK")
    with ExitStack():
        yield init_app(init_db=False)

@pytest.fixture
def client(app):
    print("CLIENT")
    with TestClient(app) as c:
        yield c

@pytest_asyncio.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    print("CREATE TABLES")
    async with sessionmanager.connect() as connection:
        await sessionmanager.drop_all(connection)
        await sessionmanager.create_all(connection)

@pytest_asyncio.fixture(scope="function", autouse=True)
async def session_override(app, connection_test):
    print("Session manager initialized:", sessionmanager._sessionmaker is not None)
    async def get_db_override():
        async with sessionmanager.session() as session:
            yield session

    app.dependency_overrides[get_db] = get_db_override

@pytest_asyncio.fixture(scope="function", autouse=True)
async def session_override(app, connection_test):
    print("Session manager initialized:", sessionmanager._sessionmaker is not None)
    async def get_db_override():
        async with sessionmanager.session() as session:
            yield session

    app.dependency_overrides[get_db] = get_db_override


@pytest_asyncio.fixture(scope="function")
async def session(connection_test):
    """Фикстура, предоставляющая асинхронную сессию для тестов."""
    async with sessionmanager.session() as session:
        yield session