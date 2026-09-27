"""FastAPI dependency wiring. get_session lives here and a route never sees
it -- the route receives a fully built service, satisfying "a route that
opens a database session is a design failure" while still using DI (plan
§10.8). This is the one non-repository, non-db module allowed to import
sqlalchemy, since threading a real AsyncSession into a repository is exactly
what it exists to do.
"""

from collections.abc import AsyncIterator

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.complaint_repository import ComplaintRepository
from app.services.stats_service import StatsService


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    async with request.app.state.sessionmaker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


def get_stats_service(request: Request, session: AsyncSession = Depends(get_session)) -> StatsService:
    return StatsService(ComplaintRepository(session), request.app.state.stats_cache)
