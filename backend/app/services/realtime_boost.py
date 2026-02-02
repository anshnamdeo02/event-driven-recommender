from datetime import datetime, timedelta
from backend.app.db.session import SessionLocal
from backend.app.models.event import Event


BOOST_MAP = {
    "like": 3,
    "view": 1,
    "skip": -2
}

WINDOW_MINUTES = 30


def get_recent_boosts(user_id):

    # 🚨 If user_id is not UUID (ML demo user), skip boosting
    if not isinstance(user_id, str):
        return {}

    db = SessionLocal()

    cutoff = datetime.utcnow() - timedelta(minutes=WINDOW_MINUTES)

    events = (
        db.query(Event)
        .filter(
            Event.user_id == user_id,
            Event.timestamp >= cutoff
        )
        .all()
    )

    boosts = {}

    for e in events:
        b = BOOST_MAP.get(e.event_type, 0)
        boosts[e.item_id] = boosts.get(e.item_id, 0) + b

    db.close()
    print(f"⚡ REAL-TIME BOOSTS for user {user_id}: {boosts}")
    return boosts
