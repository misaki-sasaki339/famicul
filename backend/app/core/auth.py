from datetime import datetime, timedelta, timezone
from jose import jwt

SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"

def create_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token