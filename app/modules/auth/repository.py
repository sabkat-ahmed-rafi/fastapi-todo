from datetime import datetime

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from .model import RefreshToken


class RefreshTokenRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def replace_for_user(
        self,
        user_id: str,
        replacement: RefreshToken,
    ) -> None:
        await self.session.execute(
            delete(RefreshToken).where(RefreshToken.user_id == user_id)
        )
        self.session.add(replacement)
        await self.session.commit()

    async def is_valid(
        self,
        token_id: str,
        user_id: str,
        token_hash: str,
        now: datetime,
    ) -> bool:
        result = await self.session.execute(
            select(RefreshToken.id).where(
                RefreshToken.id == token_id,
                RefreshToken.user_id == user_id,
                RefreshToken.token_hash == token_hash,
                RefreshToken.expires_at > now,
            )
        )
        return result.scalar_one_or_none() is not None

    async def delete(
        self,
        token_id: str,
        user_id: str,
        token_hash: str,
    ) -> bool:
        result = await self.session.execute(
            delete(RefreshToken).where(
                RefreshToken.id == token_id,
                RefreshToken.user_id == user_id,
                RefreshToken.token_hash == token_hash,
            )
        )
        await self.session.commit()
        return result.rowcount == 1
