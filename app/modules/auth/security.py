from datetime import datetime, timezone

import jwt

from core.config import settings
from .exceptions import TokenExpired


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def encode_access_token(user_id: str) -> str:
    expire = int(datetime.now(timezone.utc).timestamp()) + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, settings.ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.ACCESS_TOKEN_SECRET, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        raise TokenExpired()
