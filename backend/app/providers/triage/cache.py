"""Redis-backed content-hash triage cache (task AI-08), fulfilling
`TriageService`'s `TriageCache` Protocol.

The key deliberately excludes `location`: nine neighbours reporting the
same burst main from different houses should cost one Groq call, not
nine, provided their complaint text matches after normalization. It
includes provider, model, and prompt version, so switching any of them
never serves a stale classification under the old scheme.

Hit/miss counters live in Redis, not in-process, for the same reason
outcomes.py's log does: with 2-10 backend replicas, an in-process counter
would only ever reflect whichever pod answered `/api/meta/providers`.
"""

import hashlib

from redis.asyncio import Redis

from app.providers.triage.base import TriageResult
from app.providers.triage.prompt import PROMPT_VERSION
from app.providers.triage.text import normalize

TTL_S = 86_400
HITS_KEY = "triage:stats:hits"
MISSES_KEY = "triage:stats:misses"


class TriageResultCache:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    def key(self, *, provider: str, model: str, text: str) -> str:
        digest = hashlib.sha256(normalize(text).encode()).hexdigest()
        return f"triage:{PROMPT_VERSION}:{provider}:{model}:{digest}"

    async def get(self, key: str) -> TriageResult | None:
        raw = await self._redis.get(key)
        if raw is None:
            await self._redis.incr(MISSES_KEY)
            return None
        await self._redis.incr(HITS_KEY)
        return TriageResult.model_validate_json(raw)

    async def set(self, key: str, result: TriageResult) -> None:
        await self._redis.set(key, result.model_dump_json(), ex=TTL_S)

    async def hit_rate(self) -> float | None:
        hits, misses = await self._redis.mget(HITS_KEY, MISSES_KEY)
        h, m = int(hits or 0), int(misses or 0)
        return None if h + m == 0 else h / (h + m)
