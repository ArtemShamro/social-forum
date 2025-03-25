# from sqlalchemy import (Column, Integer, MetaData, String, Table,
#                         create_engine, ARRAY, Date, DateTime)
from sqlalchemy import ForeignKey, text, Text, Date, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, date
# from typing import Annotated
import contextlib
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncAttrs, AsyncConnection, AsyncEngine
from sqlalchemy.orm import DeclarativeBase, declared_attr
from app.api.config import Config
from contextlib import asynccontextmanager
import os
from typing import AsyncGenerator, AsyncIterator

# DATABASE_URL = os.getenv('DATABASE_URL')
# # DATABASE_URL = 'postgresql://movie_user:movie_password@localhost/movie_db'

# engine = create_async_engine(DATABASE_URL)
# async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: async_sessionmaker | None = None

    def init(self, host: str):
        self._engine = create_async_engine(host)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    # Used for testing
    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)

sessionmanager = DatabaseSessionManager()

# async def init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmanager.session() as session:
        yield session
