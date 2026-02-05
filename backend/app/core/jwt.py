from jose import jwt
from datetime import datetime, timedelta

SECRET = "super-secret-key"

def create_token(user_id: str):
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")
