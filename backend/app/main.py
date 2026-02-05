from fastapi import FastAPI
from backend.app.api.health import router as health_router
from backend.app.api.users import router as users_router
from backend.app.api.items import router as items_router
from backend.app.api.events import router as events_router
from backend.app.api.recommendations import router as recommendations_router
from backend.app.api.ml_recommendations import router as ml_router
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api import auth

app = FastAPI(title="Event-Driven Recommendation System")

app.include_router(health_router)
app.include_router(users_router)
app.include_router(items_router)
app.include_router(events_router)
app.include_router(recommendations_router)
app.include_router(ml_router)
app.include_router(auth.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)