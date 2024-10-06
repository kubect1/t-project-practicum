from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    chat_id: Optional[int] = Field(None)


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True
