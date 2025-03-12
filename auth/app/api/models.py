from sqlalchemy import text, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from sqlalchemy import func

from app.api.db import Base

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