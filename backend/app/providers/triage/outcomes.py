"""Redis-backed outcome log (task AI-10), fulfilling `TriageService`'s
`OutcomeSink` Protocol. Redis, not an in-process deque: with 2-10 backend
replicas, an in-process list would show only whichever pod happened to
answer `/api/meta/providers` -- the same distributed-state argument as
CA-02's rate limiter.
"""

from collections.abc import Awaitable
from datetime import UTC, datetime
from typing import cast
from uuid import UUID

from redis.asyncio import Redis

from app.schemas import TriageOutcomeOut
from app.services.triage_service import TriageOutcome

KEY = "triage:outcomes"
MAX_ENTRIES = 20


class OutcomeLog:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def record(self, complaint_id: UUID, outcome: TriageOutcome) -> None:
        entry = TriageOutcomeOut(
            complaint_id=complaint_id,
            provider=outcome.triaged_by,
            latency_ms=outcome.latency_ms,
            fallback=outcome.fallback,
            cache_hit=outcome.cache_hit,
            error_class=outcome.error_class,
            at=datetime.now(UTC),
        )
        async with self._redis.pipeline(transaction=True) as pipe:
            pipe.lpush(KEY, entry.model_dump_json())
            pipe.ltrim(KEY, 0, MAX_ENTRIES - 1)
            await pipe.execute()

    async def recent(self) -> list[dict[str, object]]:
        # redis-py's stubs type lrange() as Awaitable[list] | list (the same
        # class backs both sync and async clients); this Redis is always the
        # asyncio one, so the awaitable branch always applies at runtime.
        call = cast("Awaitable[list[str]]", self._redis.lrange(KEY, 0, MAX_ENTRIES - 1))
        raw = await call
        return [TriageOutcomeOut.model_validate_json(r).model_dump(mode="json") for r in raw]
