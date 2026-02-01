import math
from datetime import datetime, timezone

EVENT_WEIGHTS = {
    "view": 1,
    "like": 3,
    "skip": -2,
}

LAMBDA = 0.1  # time decay factor


def time_decay(timestamp):
    now = datetime.now(timezone.utc)
    days = (now - timestamp).days
    return math.exp(-LAMBDA * days)


def watch_time_weight(watch_time, duration):
    if not duration or duration == 0:
        return 0

    ratio = watch_time / duration

    if ratio < 0.2:
        return 0
    elif ratio < 0.5:
        return 1
    elif ratio < 0.8:
        return 2
    else:
        return 3


def compute_signal(event, item_duration=None):
    base = 0

    if event.event_type == "watch_time":
        base = watch_time_weight(event.event_value or 0, item_duration)
    else:
        base = EVENT_WEIGHTS.get(event.event_type, 0)

    decay = time_decay(event.timestamp)

    return base * decay
