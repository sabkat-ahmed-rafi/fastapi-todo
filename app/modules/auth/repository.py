from datetime import datetime

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from .model import RefreshToken


class RefreshTokenRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, refresh_token: RefreshToken) -> RefreshToken:
        self.session.add(refresh_token)
        await self.session.commit()
        await self.session.refresh(refresh_token)
        return refresh_token

    async def rotate(
        self,
        token_id: str,
        user_id: str,
        token_hash: str,
        now: datetime,
        replacement: RefreshToken,
    ) -> bool:
        # A conditional delete makes concurrent reuse safe: only one request can
        # consume the current refresh token and persist its replacement.
        result = await self.session.execute(
            delete(RefreshToken).where(
                RefreshToken.id == token_id,
                RefreshToken.user_id == user_id,
                RefreshToken.token_hash == token_hash,
                RefreshToken.expires_at > now,
            )
        )
        if result.rowcount != 1:
            await self.session.rollback()
            return False

        self.session.add(replacement)
        await self.session.commit()
        return True
