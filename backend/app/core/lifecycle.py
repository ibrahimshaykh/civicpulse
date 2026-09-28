"""App lifespan: opens the Postgres and Redis pools once at startup, closes
them once at shutdown, and exposes a `shutting_down` flag that /ready and
BE-06's graceful drain read.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import Settings
from app.db.session import build_engine, build_sessionmaker
from app.providers.cache import StatsCache
from app.providers.rate_limiter import RedisFixedWindowLimiter
from app.providers.redis_client import build_redis_client
from app.providers.triage.factory import build_triage_service

shutting_down = False


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    global shutting_down
    shutting_down = False

    settings: Settings = app.state.settings
    engine = build_engine(settings)
    app.state.engine = engine
    app.state.sessionmaker = build_sessionmaker(engine)

    redis = build_redis_client(settings)
    app.state.redis = redis
    app.state.stats_cache = StatsCache(redis, ttl_s=settings.stats_cache_ttl_s)
    app.state.rate_limiter = RedisFixedWindowLimiter(
        redis, limit=settings.rate_limit_per_window, window_s=settings.rate_limit_window_s
    )
    app.state.triage_service = build_triage_service(settings, redis)

    yield

    # BE-06's GracefulServer flips `shutting_down` the moment SIGTERM arrives,
    # well before this line runs -- uvicorn only resumes the lifespan (and
    # reaches this point) once every in-flight request has already drained.
    # This assignment is a safety net for callers that never go through
    # GracefulServer at all (TestClient, `uvicorn app.main:app` directly).
    shutting_down = True
    await redis.aclose()
    await engine.dispose()
