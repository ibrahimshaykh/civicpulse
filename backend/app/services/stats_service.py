from datetime import UTC, datetime
from typing import Literal

from app.providers.cache import StatsCache
from app.repositories.complaint_repository import ComplaintRepository
from app.schemas import StatsOut

CacheState = Literal["HIT", "MISS"]


class StatsService:
    def __init__(self, repo: ComplaintRepository, cache: StatsCache) -> None:
        self._repo = repo
        self._cache = cache

    async def get(self) -> tuple[StatsOut, CacheState]:
        cached = await self._cache.get()
        if cached is not None:
            return cached, "HIT"
        agg = await self._repo.aggregate()
        fresh = StatsOut(
            total=agg.total,
            by_category=agg.by_category,
            by_priority=agg.by_priority,
            by_status=agg.by_status,
            generated_at=datetime.now(UTC),
        )
        await self._cache.set(fresh)
        return fresh, "MISS"

    async def invalidate(self) -> None:
        """Called after a create/status-change commit, never before (plan
        §10.6): invalidating before a commit that then fails would let a
        concurrent reader re-populate the cache with the stale pre-write value.
        """
        await self._cache.invalidate()
