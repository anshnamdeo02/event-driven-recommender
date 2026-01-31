from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class RecommendationResponse(BaseModel):
    user_id: UUID
    item_id: int
    score: float
    source: str
    generated_at: datetime

    class Config:
        from_attributes = True
