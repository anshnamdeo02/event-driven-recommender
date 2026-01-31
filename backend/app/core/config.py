from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    app_name: str = "Event-Driven Recommender"
    environment: str = "local"
    database_url: str

    class Config:
        env_file = BASE_DIR / "backend" / ".env"

settings = Settings()
