from pydantic import BaseModel, Field


class Route(BaseModel):
    distance: int = Field(...)
    duration: int = Field(...)

