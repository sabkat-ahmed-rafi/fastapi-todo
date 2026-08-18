from users.schemas import UserCreate, UserResponse
from users.service import UserService

from ..schemas import RegisterRequest


class RegistrationService:

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def register(self, data: RegisterRequest) -> UserResponse:
        return await self.user_service.create_user(
            UserCreate(**data.model_dump())
        )
