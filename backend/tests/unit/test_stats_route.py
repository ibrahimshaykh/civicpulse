"""The real /api/stats route (CA-01), tested via FastAPI's own
dependency_overrides -- the standard way to test a route in isolation from
the infrastructure its dependencies would otherwise need, not a workaround
for missing Docker. A live request that actually reaches Redis/Postgres is a
separate, still-open gap (see test_stats_cache.py's docstring)."""

from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.api.deps import get_stats_service
from app.main import create_app
from app.schemas import StatsOut

STATS = StatsOut(
    total=3,
    by_category={"water": 1, "electricity": 0, "sanitation": 0, "roads": 0, "streetlights": 0, "other": 2},
    by_priority={"high": 1, "normal": 2, "low": 0},
    by_status={"open": 2, "in_progress": 0, "resolved": 1, "rejected": 0},
    generated_at=datetime.now(UTC),
)


class FakeStatsService:
    def __init__(self, cache_state: str) -> None:
        self._cache_state = cache_state

    async def get(self) -> tuple[StatsOut, str]:
        return STATS, self._cache_state


def _client_with_fake_stats(cache_state: str) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_stats_service] = lambda: FakeStatsService(cache_state)
    return TestClient(app)


def test_stats_route_reports_a_cache_hit() -> None:
    client = _client_with_fake_stats("HIT")
    response = client.get("/api/stats")
    assert response.status_code == 200
    assert response.headers["X-Cache"] == "HIT"
    assert response.headers["Cache-Control"] == "no-store"
    assert response.json()["total"] == 3


def test_stats_route_reports_a_cache_miss() -> None:
    client = _client_with_fake_stats("MISS")
    response = client.get("/api/stats")
    assert response.headers["X-Cache"] == "MISS"
