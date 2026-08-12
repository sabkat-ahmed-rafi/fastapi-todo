from fastapi import Cookie, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.config import settings
from .security import decode_access_token
from .service import AuthService
from .exceptions import InactiveUser, InvalidCredentials, TokenExpired
from users.service import UserService
from users.dependencies import get_user_service
from users.model import Users

security = HTTPBearer(auto_error=False)


def get_auth_service(
    user_service: UserService = Depends(get_user_service),
):
    return AuthService(user_service=user_service)


async def verify_api_key(
    x_api_key: str = Header(alias="X-API-Key"),
):
    if x_api_key != settings.API_KEY:
        raise InvalidCredentials("Invalid or missing API key")
    return True


async def verify_token(
    access_token: str | None = Cookie(default=None),
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict:
    token = access_token or (credentials.credentials if credentials else None)
    if not token:
        raise InvalidCredentials("Missing token")
    try:
        return decode_access_token(token)
    except TokenExpired:
        raise


async def get_current_user(
    token: dict = Depends(verify_token),
    user_service: UserService = Depends(get_user_service),
) -> Users:
    user = await user_service.get_by_id(token["sub"])
    if not user:
        raise InvalidCredentials()
    return user


async def get_current_active_user(
    user: Users = Depends(get_current_user),
) -> Users:
    if not user.is_active:
        raise InactiveUser()
    return user
