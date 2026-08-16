from datetime import datetime, timezone

from .model import RefreshToken
from .repository import RefreshTokenRepository
from .schemas import LoginRequest, RegisterRequest, Token, LoginResponse
from .security import create_refresh_token, encode_access_token, hash_refresh_token
from users.service import UserService
from users.schemas import UserCreate, UserResponse
from users.security import verify_password
from .exceptions import InactiveUser, InvalidCredentials


class AuthService:

    def __init__(
        self,
        user_service: UserService,
        refresh_token_repository: RefreshTokenRepository,
    ):
        self.user_service = user_service
        self.refresh_token_repository = refresh_token_repository


    async def register(self, data: RegisterRequest) -> UserResponse:
        return await self.user_service.create_user(UserCreate(**data.model_dump()))


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
        await self.refresh_token_repository.create(
            RefreshToken(
                id=token_id,
                user_id=user_id,
                token_hash=hash_refresh_token(refresh_token),
                expires_at=expires_at,
            )
        )
        return Token(
            access_token=encode_access_token(user_id),
            refresh_token=refresh_token,
        )


    async def rotate_refresh_token(self, token: str, payload: dict) -> Token:
        user_id = payload["sub"]
        user = await self.user_service.get_by_id(user_id)
        if not user:
            raise InvalidCredentials()
        if not user.is_active:
            raise InactiveUser()

        refresh_token, token_id, expires_at = create_refresh_token(user.id)
        replacement = RefreshToken(
            id=token_id,
            user_id=user.id,
            token_hash=hash_refresh_token(refresh_token),
            expires_at=expires_at,
        )
        rotated = await self.refresh_token_repository.rotate(
            token_id=payload["jti"],
            user_id=user.id,
            token_hash=hash_refresh_token(token),
            now=datetime.now(timezone.utc),
            replacement=replacement,
        )
        if not rotated:
            raise InvalidCredentials("Invalid or already used refresh token")

        return Token(
            access_token=encode_access_token(user.id),
            refresh_token=refresh_token,
        )
