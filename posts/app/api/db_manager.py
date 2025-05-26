from fastapi import Depends
from app.api import schemas
from sqlalchemy import select, or_, func
import app.api.models as db
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.db import get_db


class PostsDB:

    @classmethod
    async def add_post(cls, payload: schemas.CreatePost,
                       session: AsyncSession = Depends(get_db)):
        new_post = db.Posts(**payload.model_dump())

        session.add(new_post)
        await session.commit()
        await session.refresh(new_post)
        return new_post
    
    @classmethod
    async def get_posts(cls, post_ids: list[int],
                        session: AsyncSession = Depends(get_db)):
        query = select(db.Posts).filter(db.Posts.id.in_(post_ids))
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_post(cls, payload: schemas.GetPost,
                       session: AsyncSession = Depends(get_db)):
        query = select(db.Posts).filter_by(id=int(payload.post_id))
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def list_posts(cls, payload: schemas.ListPosts,
                         session: AsyncSession):
        query = select(db.Posts).filter(
            or_(db.Posts.owner_id == payload.owner_id,
                db.Posts.private == False)
        ).order_by(db.Posts.created_at.desc())

        # Get total count before applying limit and offset
        total_count_query = select(func.count()).select_from(query.subquery())
        total_count_result = await session.execute(total_count_query)
        total_count = total_count_result.scalar_one()

        query = query.offset((payload.page - 1) * payload.per_page).limit(payload.per_page)

        result = await session.execute(query)
        posts = result.scalars().all()

        return posts, total_count

    @classmethod
    async def update_post(cls, payload: schemas.UpdatePost, id: int,
                          session: AsyncSession) -> db.Posts | None:
        try:
            post = await session.get(db.Posts, id)
            if post is None:
                return None

            update_data = payload.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                if value is not None:
                    setattr(post, key, value)

            await session.commit()
            await session.refresh(post)

            return post

        except Exception as e:
            await session.rollback()
            raise e

    @classmethod
    async def delete_post(cls, id: int,
                          session: AsyncSession) -> db.Posts | None:
        try:
            post = await session.get(db.Posts, id)
            if post is None:
                return None

            await session.delete(post)
            await session.commit()

            return post

        except Exception as e:
            await session.rollback()
            raise e

    @classmethod
    async def like_post(cls, payload: schemas.LikePost,
                        session: AsyncSession = Depends(get_db)):
        new_like = db.Likes(**payload.model_dump())

        session.add(new_like)
        await session.commit()
        await session.refresh(new_like)
        return

    @classmethod
    async def create_comment(cls, payload: schemas.CreateComment,
                             session: AsyncSession = Depends(get_db)):
        new_comment = db.Comments(**payload.model_dump())

        session.add(new_comment)
        await session.commit()
        await session.refresh(new_comment)
        return

    @classmethod
    async def list_comments(cls, payload: schemas.GetPostComments,
                            session: AsyncSession):
        query = select(db.Comments).filter(
            db.Comments.post_id == payload.post_id
        ).order_by(db.Comments.created_at.desc())

        query = query.offset((payload.page - 1) * payload.per_page).limit(payload.per_page)

        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def list_posts_ids(cls, session: AsyncSession):
        query = select(db.Posts.id)
        result = await session.execute(query)
        return result.scalars().all()
