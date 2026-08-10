from fastapi import Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.config import settings
from .security import decode_access_token
from .service import AuthService
from .exceptions import InactiveUser, InvalidCredentials
from users.service import UserService
from users.dependencies import get_user_service
from users.model import Users

security = HTTPBearer()


def get_auth_service(
    user_service: UserService = Depends(get_user_service),
):
    return AuthService(user_service=user_service)


async def verify_api_key(
    x_api_key: str = Header(alias="X-API-Key"),
):
    if x_api_key != settings.APP_API_KEY:
        raise InvalidCredentials()
    return True


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


async def get_current_active_user(
    user: Users = Depends(get_current_user),
) -> Users:
    if not user.is_active:
        raise InactiveUser()
    return user
