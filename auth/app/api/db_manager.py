from fastapi import Depends, HTTPException, status  
from app.api import schemas 
from sqlalchemy import select, update
import app.api.models as db
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.db import get_db

class UserDB:
    
    @classmethod
    async def add_user(cls, payload: schemas.UserRegistration,
                       session: AsyncSession = Depends(get_db)):
        new_user = db.User(**payload.model_dump())

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    @classmethod
    async def update_user(cls, payload : schemas.UserUpdate, id: int,
                       session: AsyncSession = Depends(get_db)):
        
        stmt = (
            update(db.User)
            .where(db.User.id == id)
            .values(**payload.model_dump(exclude_unset=True)) 
        )
        
        await session.execute(stmt)
        await session.commit()
        return id

    @classmethod
    async def find_one_or_none_by_login(cls, data_login: str,
                       session: AsyncSession = Depends(get_db)):
        query = select(db.User).filter_by(login=data_login)
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int,
                session: AsyncSession = Depends(get_db)):
        
        query = select(db.User).filter_by(id=data_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_all_users(cls, session: AsyncSession = Depends(get_db)):
        query = select(db.User)
        result = await session.execute(query)
        users = result.scalars().all()
        return users