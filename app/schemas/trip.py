from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any
from enum import Enum

class TransportEnum(str, Enum):
    subway = 1
    bus = 2
    car = 3
    train = 4
    plane = 5

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

    def __str__(self):
        return self.from_place_title + '  -->  ' + self.to_place_title + ' : ' + f'At {self.travel_date}'

    
