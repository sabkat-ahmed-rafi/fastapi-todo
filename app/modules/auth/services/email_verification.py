import uuid
from datetime import datetime, timedelta, timezone

from core.config import settings
from infrastructure.email import EmailService
from infrastructure.email.exceptions import EmailDeliveryFailed
from modules.users.service import UserService

from ..exceptions import EmailAlreadyVerified, InvalidEmailVerification
from ..models.email_verification_token import EmailVerificationToken
from ..repositories.email_verification import EmailVerificationRepository
from ..schemas import ResendVerificationRequest, VerifyEmailRequest
from ..security import (
    EMAIL_VERIFICATION_RESEND_COOLDOWN_SECONDS,
    EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES,
    create_email_verification_token,
    hash_email_verification_token,
)


class EmailVerificationService:

    def __init__(
        self,
        user_service: UserService,
        repository: EmailVerificationRepository,
        email_service: EmailService,
    ):
        self.user_service = user_service
        self.repository = repository
        self.email_service = email_service

    async def send_for_user(
        self,
        *,
        user_id: str,
        email: str,
        first_name: str | None = None,
    ) -> None:
        now = datetime.now(timezone.utc)
        token, token_hash = create_email_verification_token()
        record = EmailVerificationToken(
            id=str(uuid.uuid4()),
            user_id=user_id,
            token_hash=token_hash,
            expires_at=now + timedelta(minutes=EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES),
            created_at=now,
            updated_at=now,
        )
        await self.repository.replace_for_user(record)

        verification_url = f"{settings.FRONTEND_URL.rstrip('/')}/verify-email?token={token}"

        try:
            await self.email_service.send_email_verification(
                recipient=email,
                recipient_name=first_name,
                verification_url=verification_url,
                expires_in_minutes=EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES,
                idempotency_key=f"email-verification/{record.id}",
            )
        except EmailDeliveryFailed:
            # Keep the token so user can still resend; delivery failure
            # is not fatal to registration / resend flow.
            pass

    async def verify_email(self, data: VerifyEmailRequest) -> None:
        now = datetime.now(timezone.utc)
        token_hash = hash_email_verification_token(data.token)
        record = await self.repository.get_by_token_hash(token_hash, now)
        if not record:
            raise InvalidEmailVerification()

        success = await self.repository.consume_for_verification(
            token_id=record.id,
            user_id=record.user_id,
            token_hash=token_hash,
            now=now,
        )
        if not success:
            raise InvalidEmailVerification()

    async def resend_verification(self, data: ResendVerificationRequest) -> None:
        user = await self.user_service.get_by_email(str(data.email))
        # Always return silently for non-existent or deleted users to avoid enumeration
        if not user or user.deleted_at is not None or not user.is_active:
            return
        if user.is_verified:
            raise EmailAlreadyVerified()

        now = datetime.now(timezone.utc)
        existing = await self.repository.get_for_user(user.id)
        if existing:
            # Enforce resend cooldown based on created_at
            if existing.created_at:
                from datetime import timedelta

                cooldown_threshold = now - timedelta(
                    seconds=EMAIL_VERIFICATION_RESEND_COOLDOWN_SECONDS
                )
                if existing.created_at > cooldown_threshold:
                    return
            # Also don't resend if token still valid and very recent — cooldown covers it
            # Otherwise we replace with a new token below

        await self.send_for_user(
            user_id=user.id,
            email=user.email,
            first_name=user.first_name,
        )
