from pydantic import BaseModel, Field
from datetime import datetime

class UserBase(BaseModel):
    chat_id: int = Field(..., )
    name: str = Field(..., min_length=3, max_length=128)
    registration_date: datetime = Field(...)

