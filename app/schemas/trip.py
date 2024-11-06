from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any, Self
from enum import Enum


class TransportEnum(str, Enum):
    subway = 1
    bus = 2
    car = 3
    train = 4
    plane = 5

class TripBase(BaseModel):
    chat_id: int = Field(...)
    to_place: dict[Any, Any] = Field(...)
    from_place: dict[Any, Any]= Field(...)
    to_place_title: str = Field(..., min_length=3, max_length=128)
    from_place_title: str = Field(..., min_length=3, max_length=128)
    transport_type: TransportEnum = Field(...)
    create_date: datetime = Field(...)
    travel_date: datetime = Field(...)
    notification_before_travel: datetime = Field(...)
    isEnded: bool = Field(...)

    def __str__(self):
        isEnded_str = ''
        if (self.isEnded):
            isEnded_str = " <=> Completed ✅"
        return (self.from_place_title + '  -->  ' + self.to_place_title + ' : ' +
                f'At {self.travel_date}' + isEnded_str)

    def get_info(self):
        return (str(self) + '\n' +
                f'time for notification before travel: {self.notification_before_travel - datetime.fromisoformat('1970-01-01')}' + '\n' +
                f'type of transport: {self.transport_type.name}')


class TripRead(TripBase):
    id: int = Field(...)

    class Config:
        from_attributes = True



