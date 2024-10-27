from typing import Optional
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class User(Base):
    __tablename__ = "user"

    chat_id: Mapped[int] = mapped_column(Integer(), primary_key = True, nullable=False)
    name: Mapped[str] = mapped_column(String(), nullable=False)
    registration_date: Mapped[DateTime] = mapped_column(DateTime(), nullable=False)
   
