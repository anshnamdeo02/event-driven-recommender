from fastapi import APIRouter, Query
from backend.app.services.ml_service import recommend_for_user
from backend.app.services.ml_service import hybrid_recommend
from backend.app.services.cache import get_cache, set_cache
from backend.app.services.realtime_boost import get_recent_boosts
router = APIRouter(prefix="/ml", tags=["ml-recommendations"])

@router.get("/recommendations")
def ml_recs(user_id: int = Query(...), k: int = 10):
    items = recommend_for_user(user_id, k)
    return {"user_id": user_id, "recommendations": items}

# @router.get("/hybrid")
# def hybrid(user_id: int, k: int = 10):
#     items = hybrid_recommend(user_id, k)
#     return {"user_id": user_id, "recommendations": items}

@router.get("/hybrid")
def hybrid(user_id: int, k: int = 10):

    cache_key = f"hybrid:{user_id}:{k}"

    cached = get_cache(cache_key)
    if cached:
        return cached

    items = hybrid_recommend(user_id, k)

    response = {
        "user_id": user_id,
        "recommendations": items
    }

    set_cache(cache_key, response)

    return response

@router.get("/debug-boosts")
def debug_boosts(user_id: str):
    return get_recent_boosts(user_id)