from sqlalchemy import Integer, String, DateTime, JSON, Boolean, ForeignKey, BigInteger, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base
from app.models.transport_enum import TransportEnum

class Trip(Base):
    __tablename__ = "trip"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    chat_id: Mapped[int] = mapped_column(BigInteger(), ForeignKey("user.chat_id"), nullable=False)
    to_place: Mapped[dict[str, str]] = mapped_column(JSON(), nullable=False)
    from_place: Mapped[dict[str, str]] = mapped_column(JSON(), nullable=False)
    to_place_title: Mapped[str] = mapped_column(String(150), nullable=False)
    from_place_title: Mapped[str] = mapped_column(String(150), nullable=False)
    transport_type: Mapped[TransportEnum] = mapped_column(String(150), nullable=False)
    create_date: Mapped[DateTime] = mapped_column(DateTime(), nullable=False)
    travel_date: Mapped[DateTime] = mapped_column(DateTime(), nullable=False)
    notification_before_travel: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(), nullable=False)
    isEnded: Mapped[bool] = mapped_column(Boolean(), nullable=False)