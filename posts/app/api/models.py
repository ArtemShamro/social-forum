from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import relationship

from app.api.db import Base


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    private: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=datetime.now)

    extend_existing = True

    comments: Mapped["Comments"] = relationship("Comments", back_populates="post")
    likes: Mapped["Likes"] = relationship("Likes", back_populates="post")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.title!r}")

    def __repr__(self):
        return str(self)


class Comments(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    owner_id: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    comment: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    extend_existing = True

    post: Mapped["Posts"] = relationship("Posts", back_populates="comments")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.title!r}")

    def __repr__(self):
        return str(self)


class Likes(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    owner_id: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    extend_existing = True

    post: Mapped["Posts"] = relationship("Posts", back_populates="likes")

    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.title}")

    def __repr__(self):
        return
