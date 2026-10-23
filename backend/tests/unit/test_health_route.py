from fastapi.testclient import TestClient

from app.api.deps import get_readiness_service
from app.main import create_app
from app.services.readiness_service import ReadinessReport


class FakeReadinessService:
    def __init__(self, report: ReadinessReport) -> None:
        self._report = report

    async def check(self) -> ReadinessReport:
        return self._report


def _client_with_fake_readiness(report: ReadinessReport) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_readiness_service] = lambda: FakeReadinessService(report)
    return TestClient(app)


def test_health_never_touches_the_database() -> None:
    # No dependency_overrides at all: if /health touched app.state.sessionmaker
    # (never built outside the lifespan), this would raise, not just be slow.
    client = TestClient(create_app())
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_is_200_when_everything_is_ok() -> None:
    client = _client_with_fake_readiness(
        ReadinessReport(ok=True, checks={"postgres": "ok", "redis": "ok"}, failed=[])
    )
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready", "checks": {"postgres": "ok", "redis": "ok"}}


def test_ready_is_503_naming_the_failed_dependency() -> None:
    client = _client_with_fake_readiness(
        ReadinessReport(
            ok=False, checks={"postgres": "error:TimeoutError", "redis": "ok"}, failed=["postgres"]
        )
    )
    response = client.get("/ready")
    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "unavailable"
    assert body["failed"] == ["postgres"]


def test_ready_is_503_while_shutting_down() -> None:
    client = _client_with_fake_readiness(
        ReadinessReport(
            ok=False, checks={"postgres": "skipped", "redis": "skipped"}, failed=["shutting_down"]
        )
    )
    response = client.get("/ready")
    assert response.status_code == 503
    assert response.json()["failed"] == ["shutting_down"]
