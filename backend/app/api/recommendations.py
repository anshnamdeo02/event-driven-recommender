from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from backend.app.db.deps import get_db
from backend.app.models.event import Event
from backend.app.models.item import Item
from backend.app.models.recommendation import Recommendation
from backend.app.schemas.recommendation import RecommendationResponse
from uuid import UUID
from datetime import datetime

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("", response_model=list[RecommendationResponse])
def get_recommendations(
    user_id: UUID = Query(...),
    limit: int = Query(default=10),
    db: Session = Depends(get_db),
):
    # 1️⃣ Clear old recommendations (simple refresh logic)
    db.query(Recommendation).filter(
        Recommendation.user_id == user_id
    ).delete()

    # 2️⃣ Check recent user events
    recent_events = (
        db.query(Event.item_id)
        .filter(Event.user_id == user_id)
        .order_by(Event.timestamp.desc())
        .limit(limit)
        .all()
    )

    item_ids = [e.item_id for e in recent_events]

    # 3️⃣ Fallback to popular items
    if not item_ids:
        items = (
            db.query(Item)
            .order_by(Item.popularity_score.desc())
            .limit(limit)
            .all()
        )
        item_ids = [i.id for i in items]

    recommendations = []
    now = datetime.utcnow()

    for rank, item_id in enumerate(item_ids):
        rec = Recommendation(
            user_id=user_id,
            item_id=item_id,
            score=1.0 / (rank + 1),  # simple ranking score
            source="dummy_v1",
            generated_at=now,
        )
        db.add(rec)
        recommendations.append(rec)

    db.commit()
    return recommendations
