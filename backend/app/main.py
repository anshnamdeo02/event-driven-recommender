from fastapi import FastAPI
from backend.app.api.health import router as health_router
from backend.app.api.users import router as users_router
from backend.app.api.items import router as items_router

app = FastAPI(title="Event-Driven Recommendation System")

app.include_router(health_router)
app.include_router(users_router)
app.include_router(items_router)
