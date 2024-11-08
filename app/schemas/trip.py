from pydantic import BaseModel, Field
from datetime import datetime
from app.models.transport_enum import TransportEnum

class Coordinates(BaseModel):
    latitude: str = Field(...)
    longitude: str = Field(...)


class TripBase(BaseModel):
    chat_id: int = Field(...)
    to_place: Coordinates = Field(...)
    from_place: Coordinates = Field(...)
    to_place_title: str = Field(..., min_length=3, max_length=128)
    from_place_title: str = Field(..., min_length=3, max_length=128)
    transport_type: TransportEnum = Field(...)
    create_date: datetime = Field(...)
    travel_date: datetime = Field(...)
    notification_before_travel: datetime = Field(...)
    isEnded: bool = Field(...)

    def __str__(self):
        return (self.from_place_title + '  -->  ' + self.to_place_title + ' : ' +
                f'At {self.travel_date}\nCompleted: {'Yes' if self.isEnded else 'No'}')

    def get_info(self):
        return (str(self) + '\n' +
                f'time for notification before travel: {self.notification_before_travel - datetime.fromisoformat('1970-01-01')}' + '\n' +
                f'type of transport: {self.transport_type.name}')


class TripRead(TripBase):
    id: int = Field(...)

    class Config:
        from_attributes = True



