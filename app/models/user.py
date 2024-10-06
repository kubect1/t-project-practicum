from typing import Optional
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    chat_id: Mapped[int] = mapped_column(Integer(), nullable=False)
