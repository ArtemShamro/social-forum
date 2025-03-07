# from sqlalchemy import (Column, Integer, MetaData, String, Table,
#                         create_engine, ARRAY, Date, DateTime)
from sqlalchemy import ForeignKey, text, Text, Date, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, date
# from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr

import os

DATABASE_URL = os.getenv('DATABASE_URL')
# DATABASE_URL = 'postgresql://movie_user:movie_password@localhost/movie_db'

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
 
class User(Base):
    id: Mapped[int] =  mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(60), unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=True)
    name: Mapped[str] = mapped_column(nullable=True)
    surname: Mapped[str] = mapped_column(nullable=True)
    birthdate: Mapped[date] = mapped_column(nullable=True)
    mail: Mapped[str]
    phone: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=datetime.now)

    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_business: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    
    extend_existing = True
    
    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.first_name!r},"
                f"last_name={self.last_name!r})")

    def __repr__(self):
        return str(self)