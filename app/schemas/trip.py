from typing import Optional
from pydantic import BaseModel, Field, Enum
from datetime import datetime
from typing import Any

class TransportEnum(str, Enum):
    subway = "Метро"
    bus = "Автобус"
    car = "Машина"
    train = "Поезд"
    plane = "Самолёт"

class TripBase(BaseModel):
    id: int = Field(...)
    chat_id: int = Field(...)
    to_place: dict[Any, Any] = Field(..., min_length=3, max_length=128)
    from_place: dict[Any, Any]= Field(..., min_length=3, max_length=128)
    to_place_title: str = Field(...)
    from_place_title: str = Field(...)
    transport_type: TransportEnum = Field(...)
    create_date: datetime = Field(...)
    travel_date: datetime = Field(...)
    notification_before_travel: datetime = Field(...)
    isEnded: bool = Field(...)

    