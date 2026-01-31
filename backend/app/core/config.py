from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Event-Driven Recommender"
    environment: str = "local"
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
