import uuid
from datetime import datetime, timedelta, timezone
from hashlib import sha256

import jwt

from core.config import settings
from .exceptions import TokenExpired


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def encode_access_token(user_id: str) -> str:
    expire = int(datetime.now(timezone.utc).timestamp()) + (ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, settings.ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.ACCESS_TOKEN_SECRET, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        raise TokenExpired()


def encode_refresh_token(
    user_id: str,
    token_id: str,
    expires_at: datetime,
) -> str:
    payload = {
        "sub": user_id,
        "jti": token_id,
        "type": "refresh",
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.REFRESH_TOKEN_SECRET, algorithm=ALGORITHM)


def decode_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.REFRESH_TOKEN_SECRET,
            algorithms=[ALGORITHM],
            options={"require": ["sub", "jti", "type", "exp"]},
        )
    except jwt.InvalidTokenError:
        raise TokenExpired()

    if payload["type"] != "refresh":
        raise TokenExpired()
    return payload


def create_refresh_token(user_id: str) -> tuple[str, str, datetime]:
    token_id = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    token = encode_refresh_token(user_id, token_id, expires_at)
    return token, token_id, expires_at


def hash_refresh_token(token: str) -> str:
    return sha256(token.encode("utf-8")).hexdigest()
