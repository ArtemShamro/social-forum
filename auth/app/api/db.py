# from sqlalchemy import (Column, Integer, MetaData, String, Table,
#                         create_engine, ARRAY, Date, DateTime)
from sqlalchemy import ForeignKey, text, Text, Date, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, date
# from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr

import os
from typing import AsyncGenerator

DATABASE_URL = os.getenv('DATABASE_URL')
# DATABASE_URL = 'postgresql://movie_user:movie_password@localhost/movie_db'

engine = create_async_engine(DATABASE_URL)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
            # try:
            #     yield session
            # finally:
            #     await session.close()
 
