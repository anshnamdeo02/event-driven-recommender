import time

CACHE = {}
TTL = 300  # 5 minutes


def get_cache(key):
    if key in CACHE:
        value, ts = CACHE[key]

        if time.time() - ts < TTL:
            return value

        del CACHE[key]

    return None


def set_cache(key, value):
    CACHE[key] = (value, time.time())


def invalidate_user(user_id):
    key = f"recs:{user_id}"
    if key in CACHE:
        del CACHE[key]
