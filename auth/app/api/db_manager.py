from app.api import models 
from sqlalchemy import select, update
import app.api.db as db
from app.api.db import async_session_maker 

class UserDB:
    @classmethod
    async def add_user(cls, payload: models.UserRegistration):
        new_student = db.User(**payload.model_dump())

        async with async_session_maker() as session:
            session.add(new_student)
            await session.commit()
            await session.refresh(new_student)
            return new_student.id

    @classmethod
    async def update_user(cls, user_data, id):
        async with async_session_maker() as session:
            
            stmt = (
                update(db.User)
                .where(db.User.id == id)
                .values(**user_data) 
            )
            
            await session.execute(stmt)
            await session.commit()

        return id

    @classmethod
    async def find_one_or_none_by_login(cls, data_login: str):
        async with async_session_maker() as session:
            query = select(db.User).filter_by(login=data_login)
            result = await session.execute(query)
            return result.scalar_one_or_none()
    
    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with async_session_maker() as session:
            query = select(db.User).filter_by(id=data_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_all_users(cls):
        async with async_session_maker() as session:
            query = select(db.User)
            result = await session.execute(query)
            users = result.scalars().all()
            return users