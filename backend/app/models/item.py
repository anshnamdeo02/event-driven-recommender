from sqlalchemy import Column, Integer, String, Float
from backend.app.db.base import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genres = Column(String)
    language = Column(String)
    duration_minutes = Column(Integer)
    release_year = Column(Integer)
    popularity_score = Column(Float, default=0.0)
    thumbnail_url = Column(String)
