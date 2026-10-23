from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class HealthRepository:
    """Even `SELECT 1` is SQL, so it lives in a repository, not the readiness
    service (plan §10.6)."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def ping_db(self) -> None:
        await self._session.execute(text("SELECT 1"))
