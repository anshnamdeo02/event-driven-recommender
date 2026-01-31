from fastapi import FastAPI
from app.api import health

app = FastAPI(title="Event-Driven Recommendation System")

app.include_router(health.router)
