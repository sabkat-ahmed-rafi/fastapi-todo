from datetime import datetime

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from modules.users.model import Users

from ..models.email_verification_token import EmailVerificationToken


class EmailVerificationRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_for_user(self, user_id: str) -> EmailVerificationToken | None:
        result = await self.session.execute(
            select(EmailVerificationToken).where(
                EmailVerificationToken.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def get_by_token_hash(
        self, token_hash: str, now: datetime
    ) -> EmailVerificationToken | None:
        result = await self.session.execute(
            select(EmailVerificationToken).where(
                EmailVerificationToken.token_hash == token_hash,
                EmailVerificationToken.expires_at > now,
            )
        )
        return result.scalar_one_or_none()

    async def replace_for_user(self, token: EmailVerificationToken) -> None:
        await self.session.execute(
            delete(EmailVerificationToken).where(
                EmailVerificationToken.user_id == token.user_id
            )
        )
        self.session.add(token)
        await self.session.commit()

    async def delete_for_user(self, user_id: str) -> None:
        await self.session.execute(
            delete(EmailVerificationToken).where(
                EmailVerificationToken.user_id == user_id
            )
        )
        await self.session.commit()

    async def consume_for_verification(
        self,
        *,
        token_id: str,
        user_id: str,
        token_hash: str,
        now: datetime,
    ) -> bool:
        """
        Atomically consume the verification token and mark the user as verified.
        Returns True only if exactly one row was affected for each step.
        """
        consumed = await self.session.execute(
            delete(EmailVerificationToken).where(
                EmailVerificationToken.id == token_id,
                EmailVerificationToken.user_id == user_id,
                EmailVerificationToken.token_hash == token_hash,
                EmailVerificationToken.expires_at > now,
            )
        )
        if consumed.rowcount != 1:
            await self.session.rollback()
            return False

        updated = await self.session.execute(
            update(Users)
            .where(
                Users.id == user_id,
                Users.is_active.is_(True),
                Users.deleted_at.is_(None),
                Users.is_verified.is_(False),
            )
            .values(is_verified=True)
        )
        if updated.rowcount != 1:
            await self.session.rollback()
            return False

        await self.session.commit()
        return True
