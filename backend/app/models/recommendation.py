from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from backend.app.db.base import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)

    score = Column(Float, nullable=False)
    source = Column(String, nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
