import structlog
from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.schemas import StatsOut

log = structlog.get_logger()


class StatsCache:
    """Read-through cache for /api/stats (plan §10.9).

    TTL and explicit invalidation together, not either alone: invalidation
    alone is only correct if every write path remembers to call it (a manual
    psql fix, a missed code path, or a failed DEL during a Redis blip would
    leave stats wrong forever); TTL alone means a citizen's new report doesn't
    show up on the dashboard for up to 30s. Together: fresh on the normal
    path, staleness bounded to the TTL on every other path.
    """

    KEY = "stats:v1"

    def __init__(self, redis: Redis, ttl_s: int) -> None:
        self._redis = redis
        self._ttl_s = ttl_s

    async def get(self) -> StatsOut | None:
        try:
            raw = await self._redis.get(self.KEY)
        except RedisError as e:
            # Fail open: a Redis blip degrades to "always compute from Postgres",
            # not to an outage. /ready still reports Redis as failed separately.
            log.warning("stats_cache_unavailable", error_class=type(e).__name__)
            return None
        return StatsOut.model_validate_json(raw) if raw else None

    async def set(self, stats: StatsOut) -> None:
        try:
            await self._redis.set(self.KEY, stats.model_dump_json(), ex=self._ttl_s)
        except RedisError as e:
            log.warning("stats_cache_unavailable", error_class=type(e).__name__)

    async def invalidate(self) -> None:
        try:
            await self._redis.delete(self.KEY)
        except RedisError as e:
            log.warning("stats_cache_unavailable", error_class=type(e).__name__)
