from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .security import decode_access_token
from .exceptions import InvalidCredentials
from users.service import UserService
from users.dependencies import get_user_service
from users.model import Users

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends(get_user_service),
) -> Users:
    token = credentials.credentials
    payload = decode_access_token(token)
    user = await user_service.get_by_id(payload["sub"])
    if not user:
        raise InvalidCredentials()
    return user


