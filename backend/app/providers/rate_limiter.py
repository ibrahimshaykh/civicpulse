"""Distributed fixed-window rate limiter (task CA-02). The counter lives in
Redis, not in an in-process dict: under an HPA of N pods, an in-process
counter would let through N times the intended limit, since each pod has
its own counter and the Service load-balances across them.
"""

import time
from dataclasses import dataclass
from typing import Protocol

import structlog
from redis.asyncio import Redis
from redis.exceptions import RedisError

from app.core.metrics import RATE_LIMITER_FAIL_OPEN

log = structlog.get_logger()

# INCR and EXPIRE in one atomic script: two separate round-trips could crash
# between them and leave a key with no TTL, which would block that client
# forever instead of for one window.
_FIXED_WINDOW_LUA = """
local current = redis.call('INCR', KEYS[1])
if current == 1 then
  redis.call('EXPIRE', KEYS[1], ARGV[1])
end
local ttl = redis.call('TTL', KEYS[1])
return {current, ttl}
"""


@dataclass(frozen=True, slots=True)
class RateDecision:
    allowed: bool
    limit: int
    remaining: int
    retry_after_s: int


class RateLimiter(Protocol):
    async def hit(self, client_id: str) -> RateDecision: ...


class RedisFixedWindowLimiter:
    name = "redis-fixed-window"

    def __init__(self, redis: Redis, *, limit: int, window_s: int) -> None:
        self._redis = redis
        self._script = redis.register_script(_FIXED_WINDOW_LUA)
        self._limit = limit
        self._window_s = window_s

    async def hit(self, client_id: str) -> RateDecision:
        window = int(time.time()) // self._window_s
        key = f"rl:complaints:{client_id}:{window}"
        try:
            count, ttl = await self._script(keys=[key], args=[self._window_s])
        except RedisError as e:
            # Fail open: a Redis blip must not turn into "nobody can submit a
            # complaint." Rate limiting degrades; the service does not.
            RATE_LIMITER_FAIL_OPEN.inc()
            log.warning("rate_limiter_fail_open", error_class=type(e).__name__)
            return RateDecision(True, self._limit, self._limit, 0)
        ttl = ttl if ttl > 0 else self._window_s
        allowed = count <= self._limit
        return RateDecision(allowed, self._limit, max(0, self._limit - count), ttl if not allowed else 0)
