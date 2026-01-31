from pydantic import BaseModel

class ItemResponse(BaseModel):
    id: int
    title: str
    genres: str | None = None
    language: str | None = None
    duration_minutes: int | None = None
    release_year: int | None = None
    popularity_score: float | None = None
    thumbnail_url: str | None = None

    class Config:
        from_attributes = True
