from .schemas import LoginRequest, RegisterRequest, Token, LoginResponse
from .security import encode_access_token
from users.service import UserService
from users.schemas import UserCreate, UserResponse
from users.security import verify_password
from .exceptions import InactiveUser, InvalidCredentials


class AuthService:

    def __init__(self, user_service: UserService):
        self.user_service = user_service


    async def register(self, data: RegisterRequest) -> UserResponse:
        return await self.user_service.create_user(UserCreate(**data.model_dump()))


    async def login(self, data: LoginRequest) -> LoginResponse:
        user = await self.user_service.get_by_email(data.email)
        if not user or not verify_password(data.password, user.password_hash):
            raise InvalidCredentials()
        if not user.is_active:
            raise InactiveUser()
        token = self._create_token(user.id)
        return LoginResponse(
            user=UserResponse.model_validate(user),
            token=token,
        )


    def _create_token(self, user_id: str) -> Token:
        return Token(
            access_token=encode_access_token(user_id),
        )
