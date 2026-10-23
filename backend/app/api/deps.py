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

from app.core import lifecycle
from app.core.errors import RateLimited
from app.repositories.complaint_repository import ComplaintRepository
from app.repositories.health_repository import HealthRepository
from app.repositories.uow import SqlAlchemyUoW
from app.services.complaint_service import ComplaintService
from app.services.meta_service import MetaService
from app.services.readiness_service import ReadinessService
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


def get_readiness_service(request: Request, session: AsyncSession = Depends(get_session)) -> ReadinessService:
    settings = request.app.state.settings
    health_repo = HealthRepository(session)
    redis = request.app.state.redis
    return ReadinessService(
        ping_db=health_repo.ping_db,
        ping_redis=redis.ping,
        timeout_s=settings.readiness_timeout_s,
        is_shutting_down=lambda: lifecycle.shutting_down,
    )


def get_complaint_service(request: Request, session: AsyncSession = Depends(get_session)) -> ComplaintService:
    st = request.app.state
    return ComplaintService(
        ComplaintRepository(session), SqlAlchemyUoW(session), st.triage_service, st.stats_cache
    )


def get_meta_service(request: Request) -> MetaService:
    st = request.app.state
    return MetaService(st.triage_service, st.settings)


def client_ip(request: Request) -> str:
    """Rightmost-untrusted X-Forwarded-For entry. The leftmost entry is
    attacker-controlled: a client can send `X-Forwarded-For: 1.2.3.4` and
    claim to be anyone, but they cannot rewrite what a *trusted* proxy hop
    appended after their own entry.
    """
    hops: int = request.app.state.settings.trusted_proxy_hops
    xff = [p.strip() for p in request.headers.get("x-forwarded-for", "").split(",") if p.strip()]
    if hops > 0 and len(xff) >= hops:
        return xff[-hops]
    return request.client.host if request.client else "unknown"


async def enforce_rate_limit(request: Request) -> None:
    decision = await request.app.state.rate_limiter.hit(client_ip(request))
    request.state.rate_limit = decision
    if not decision.allowed:
        raise RateLimited(decision.retry_after_s)
