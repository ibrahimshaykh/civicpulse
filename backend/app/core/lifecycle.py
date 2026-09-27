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
from app.providers.redis_client import build_redis_client

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

    yield

    shutting_down = True
    await redis.aclose()
    await engine.dispose()
