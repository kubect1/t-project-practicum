from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    latitude: str = Field(...)
    longitude: str = Field(...)
