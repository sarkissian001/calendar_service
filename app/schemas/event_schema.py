from pydantic import BaseModel
from datetime import datetime


class EventBase(BaseModel):
    description: str
    time: datetime


class CreateEvent(EventBase):
    class Config:
        orm_mode = True


class EventResponse(BaseModel):
    id: int
    description: str
    time: str  # Change to string since it's formatted manually

    class Config:
        orm_mode = True
