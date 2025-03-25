from sqlalchemy import text, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from sqlalchemy import func

from app.api.db import Base

class Posts(Base):
    id: Mapped[int] =  mapped_column(primary_key=True)
    owner_id: Mapped[str] = mapped_column(String(60), unique=False, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    private: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=datetime.now)

    extend_existing = True
    
    def __str__(self):
        return (f"{self.__class__.__name__}(id={self.id}, "
                f"first_name={self.title!r}")

    def __repr__(self):
        return str(self)