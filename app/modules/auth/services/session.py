from datetime import datetime, timezone

from users.schemas import UserResponse
from users.security import verify_password
from users.service import UserService

from ..exceptions import InactiveUser, InvalidCredentials
from ..models.refresh_token import RefreshToken
from ..repositories.refresh_token import RefreshTokenRepository
from ..schemas import AccessToken, LoginRequest, LoginResponse, Token
from ..security import (
    create_refresh_token,
    encode_access_token,
    hash_refresh_token,
)


class SessionService:

    def __init__(
        self,
        user_service: UserService,
        refresh_token_repository: RefreshTokenRepository,
    ):
        self.user_service = user_service
        self.refresh_token_repository = refresh_token_repository

    async def login(self, data: LoginRequest) -> LoginResponse:
        user = await self.user_service.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise InvalidCredentials()
        if not user.is_active:
            raise InactiveUser()
        token = await self._create_token(user.id)
        return LoginResponse(
            user=UserResponse.model_validate(user),
            token=token,
        )

    async def _create_token(self, user_id: str) -> Token:
        refresh_token, token_id, expires_at = create_refresh_token(user_id)
        replacement = RefreshToken(
            id=token_id,
            user_id=user_id,
            token_hash=hash_refresh_token(refresh_token),
            expires_at=expires_at,
        )
        await self.refresh_token_repository.replace_for_user(
            user_id=user_id,
            replacement=replacement,
        )
        return Token(
            access_token=encode_access_token(user_id),
            refresh_token=refresh_token,
        )

    async def refresh_access_token(self, token: str, payload: dict) -> AccessToken:
        user_id = payload["sub"]
        user = await self.user_service.get_by_id(user_id)
        if not user:
            raise InvalidCredentials()
        if not user.is_active:
            raise InactiveUser()

        is_valid = await self.refresh_token_repository.is_valid(
            token_id=payload["jti"],
            user_id=user.id,
            token_hash=hash_refresh_token(token),
            now=datetime.now(timezone.utc),
        )
        if not is_valid:
            raise InvalidCredentials("Invalid refresh token")

        return AccessToken(access_token=encode_access_token(user.id))

    async def logout(self, token: str, payload: dict) -> None:
        deleted = await self.refresh_token_repository.delete(
            token_id=payload["jti"],
            user_id=payload["sub"],
            token_hash=hash_refresh_token(token),
        )
        if not deleted:
            raise InvalidCredentials("Invalid refresh token")
