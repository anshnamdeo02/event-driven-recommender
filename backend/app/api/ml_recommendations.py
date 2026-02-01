from fastapi import APIRouter, Query
from backend.app.services.ml_service import recommend_for_user
from backend.app.services.ml_service import hybrid_recommend

router = APIRouter(prefix="/ml", tags=["ml-recommendations"])

@router.get("/recommendations")
def ml_recs(user_id: int = Query(...), k: int = 10):
    items = recommend_for_user(user_id, k)
    return {"user_id": user_id, "recommendations": items}

@router.get("/hybrid")
def hybrid(user_id: int, k: int = 10):
    items = hybrid_recommend(user_id, k)
    return {"user_id": user_id, "recommendations": items}
