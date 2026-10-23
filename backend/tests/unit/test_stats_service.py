from dataclasses import dataclass, field

from app.domain.enums import Category, Priority, Status
from app.domain.records import StatsAggregate
from app.services.stats_service import StatsService


@dataclass
class FakeCache:
    cached: object | None = None
    invalidated: bool = False
    set_calls: list[object] = field(default_factory=list)

    async def get(self) -> object | None:
        return self.cached

    async def set(self, stats: object) -> None:
        self.set_calls.append(stats)

    async def invalidate(self) -> None:
        self.invalidated = True


class FakeRepo:
    def __init__(self, aggregate: StatsAggregate) -> None:
        self._aggregate = aggregate
        self.calls = 0

    async def aggregate(self) -> StatsAggregate:
        self.calls += 1
        return self._aggregate


def _aggregate() -> StatsAggregate:
    return StatsAggregate(
        total=2,
        by_category=dict.fromkeys(Category, 0) | {Category.water: 2},
        by_priority=dict.fromkeys(Priority, 0) | {Priority.high: 2},
        by_status=dict.fromkeys(Status, 0) | {Status.open: 2},
    )


async def test_cache_hit_never_touches_the_repository() -> None:
    from app.schemas import StatsOut

    cached = StatsOut(
        total=9,
        by_category=dict.fromkeys(Category, 0),
        by_priority=dict.fromkeys(Priority, 0),
        by_status=dict.fromkeys(Status, 0),
        generated_at="2026-01-01T00:00:00Z",
    )
    cache = FakeCache(cached=cached)
    repo = FakeRepo(_aggregate())

    stats, cache_state = await StatsService(repo, cache).get()  # type: ignore[arg-type]

    assert cache_state == "HIT"
    assert stats.total == 9
    assert repo.calls == 0


async def test_cache_miss_computes_from_the_repository_and_populates_the_cache() -> None:
    cache = FakeCache()
    repo = FakeRepo(_aggregate())

    stats, cache_state = await StatsService(repo, cache).get()  # type: ignore[arg-type]

    assert cache_state == "MISS"
    assert stats.total == 2
    assert stats.by_category[Category.water] == 2
    assert repo.calls == 1
    assert len(cache.set_calls) == 1


async def test_invalidate_delegates_to_the_cache() -> None:
    cache = FakeCache()
    repo = FakeRepo(_aggregate())
    await StatsService(repo, cache).invalidate()  # type: ignore[arg-type]
    assert cache.invalidated is True
