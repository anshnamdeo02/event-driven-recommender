from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.db.deps import get_db
from backend.app.models.event import Event
from backend.app.schemas.event import EventCreate, EventResponse
from uuid import UUID
from backend.app.services.cache import invalidate_user



router = APIRouter(prefix="/events", tags=["events"])

VALID_EVENT_TYPES = {"view", "like", "watch_time", "skip"}

@router.post("", response_model=EventResponse)
def log_event(payload: EventCreate, db: Session = Depends(get_db)):
    if payload.event_type not in VALID_EVENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid event type")

    if payload.event_type == "watch_time" and payload.event_value is None:
        raise HTTPException(status_code=400, detail="watch_time requires event_value")

    event = Event(
        user_id=payload.user_id,
        item_id=payload.item_id,
        event_type=payload.event_type,
        event_value=payload.event_value
    )

    db.add(event)
    db.commit()
    invalidate_user(str(event.user_id))
    db.refresh(event)
    return event


@router.get("", response_model=list[EventResponse])
def list_events(
    user_id: UUID | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(Event)
    if user_id:
        query = query.filter(Event.user_id == user_id)
    return query.order_by(Event.timestamp.desc()).all()
