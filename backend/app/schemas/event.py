from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class EventCreate(BaseModel):
    user_id: UUID
    item_id: int
    event_type: str
    event_value: Optional[float] = None

class EventResponse(BaseModel):
    id: UUID
    user_id: UUID
    item_id: int
    event_type: str
    event_value: Optional[float]
    timestamp: datetime

    class Config:
        from_attributes = True
