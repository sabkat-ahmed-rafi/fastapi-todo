from typing import TYPE_CHECKING

from modules.users.schemas import UserCreate, UserResponse
from modules.users.service import UserService

from ..schemas import RegisterRequest

if TYPE_CHECKING:
    from .email_verification import EmailVerificationService


class RegistrationService:

    def __init__(
        self,
        user_service: UserService,
        email_verification_service: "EmailVerificationService | None" = None,
    ):
        self.user_service = user_service
        self.email_verification_service = email_verification_service

    async def register(self, data: RegisterRequest) -> UserResponse:
        user = await self.user_service.create_user(
            UserCreate(**data.model_dump())
        )
        # Send verification email after successful user creation.
        # Failures to send are non-fatal; user can resend via the resend endpoint.
        if self.email_verification_service is not None:
            await self.email_verification_service.send_for_user(
                user_id=user.id,
                email=user.email,
                first_name=user.first_name,
            )
        return user
