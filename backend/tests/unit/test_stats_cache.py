"""StatsCache against fakeredis: an in-process Redis-protocol implementation,
not a hand-rolled fake, so this exercises the real get/set/delete/TTL
semantics -- as close to "real Redis" as this sandbox (no Docker) allows.
What's still unverified without Docker: the actual 30s TTL expiring in real
time under load, and multi-pod behaviour (N pods sharing one Redis).
"""

from fakeredis.aioredis import FakeRedis
from redis.exceptions import RedisError

from app.providers.cache import StatsCache
from app.schemas import StatsOut

STATS = StatsOut(
    total=1,
    by_category={"water": 1, "electricity": 0, "sanitation": 0, "roads": 0, "streetlights": 0, "other": 0},
    by_priority={"high": 1, "normal": 0, "low": 0},
    by_status={"open": 1, "in_progress": 0, "resolved": 0, "rejected": 0},
    generated_at="2026-01-01T00:00:00Z",
)


async def test_get_on_an_empty_cache_returns_none() -> None:
    cache = StatsCache(FakeRedis(), ttl_s=30)
    assert await cache.get() is None


async def test_set_then_get_round_trips() -> None:
    cache = StatsCache(FakeRedis(), ttl_s=30)
    await cache.set(STATS)
    cached = await cache.get()
    assert cached == STATS


async def test_set_applies_the_configured_ttl() -> None:
    redis = FakeRedis()
    cache = StatsCache(redis, ttl_s=30)
    await cache.set(STATS)
    ttl = await redis.ttl(StatsCache.KEY)
    assert 0 < ttl <= 30


async def test_invalidate_removes_the_key() -> None:
    redis = FakeRedis()
    cache = StatsCache(redis, ttl_s=30)
    await cache.set(STATS)
    await cache.invalidate()
    assert await cache.get() is None


class _BrokenRedis(FakeRedis):
    async def get(self, *args: object, **kwargs: object) -> None:
        raise RedisError("connection refused")

    async def set(self, *args: object, **kwargs: object) -> None:
        raise RedisError("connection refused")

    async def delete(self, *args: object, **kwargs: object) -> None:
        raise RedisError("connection refused")


async def test_get_fails_open_when_redis_is_unavailable() -> None:
    cache = StatsCache(_BrokenRedis(), ttl_s=30)
    assert await cache.get() is None  # not an exception -- the caller falls back to computing from Postgres


async def test_set_swallows_a_redis_error() -> None:
    cache = StatsCache(_BrokenRedis(), ttl_s=30)
    await cache.set(STATS)  # must not raise


async def test_invalidate_swallows_a_redis_error() -> None:
    cache = StatsCache(_BrokenRedis(), ttl_s=30)
    await cache.invalidate()  # must not raise
