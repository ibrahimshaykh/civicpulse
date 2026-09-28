"""BE-03/BE-04/CA-02 route-level acceptance, tested via dependency_overrides
(same approach as test_stats_route.py): a route that only parses, delegates
and serializes needs a fake service, not a live database."""

from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from app.api.deps import enforce_rate_limit, get_complaint_service
from app.core.errors import InvalidTransition, NotFound
from app.domain.enums import Category, Priority, Status
from app.main import create_app
from app.schemas import ComplaintCreate, ComplaintOut, ComplaintPage
from app.services.complaint_service import ComplaintQuery

OUT = ComplaintOut(
    id=uuid4(),
    text="A pothole on the main road",
    location="Street 12",
    reporter_contact=None,
    category=Category.roads,
    priority=Priority.normal,
    status=Status.open,
    ai_summary="A pothole was reported.",
    triaged_by="rules",
    triage_latency_ms=1,
    triage_confidence=Decimal("0.5"),
    created_at=datetime(2026, 1, 1, tzinfo=UTC),
    updated_at=datetime(2026, 1, 1, tzinfo=UTC),
    allowed_transitions=[Status.in_progress, Status.rejected],
)


class FakeComplaintService:
    def __init__(self) -> None:
        self.created_with: ComplaintCreate | None = None
        self.change_status_calls: list[tuple[UUID, Status]] = []

    async def create(self, data: ComplaintCreate) -> ComplaintOut:
        self.created_with = data
        return OUT

    async def get(self, complaint_id: UUID) -> ComplaintOut:
        if complaint_id != OUT.id:
            raise NotFound(f"No complaint with id {complaint_id}")
        return OUT

    async def list(self, q: ComplaintQuery) -> ComplaintPage:
        return ComplaintPage(items=[OUT], total=1, page=q.page, page_size=q.page_size, pages=1)

    async def change_status(self, complaint_id: UUID, target: Status) -> ComplaintOut:
        self.change_status_calls.append((complaint_id, target))
        if target == Status.open:
            raise InvalidTransition(Status.resolved, Status.open, [])
        return OUT.model_copy(update={"status": target})


def _client(fake: FakeComplaintService) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_complaint_service] = lambda: fake
    app.dependency_overrides[enforce_rate_limit] = lambda: None
    return TestClient(app)


def test_create_returns_201_with_location_header() -> None:
    fake = FakeComplaintService()
    client = _client(fake)
    body = {"text": "Burst water main flooding homes", "location": "Street 12"}
    response = client.post("/api/complaints", json=body)
    assert response.status_code == 201
    assert response.headers["Location"] == f"/api/complaints/{OUT.id}"
    assert fake.created_with is not None
    assert fake.created_with.text == "Burst water main flooding homes"


def test_get_missing_complaint_returns_404_envelope() -> None:
    client = _client(FakeComplaintService())
    response = client.get(f"/api/complaints/{uuid4()}")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"


def test_get_existing_complaint_returns_200() -> None:
    client = _client(FakeComplaintService())
    response = client.get(f"/api/complaints/{OUT.id}")
    assert response.status_code == 200
    assert response.json()["id"] == str(OUT.id)


def test_list_returns_the_page() -> None:
    client = _client(FakeComplaintService())
    response = client.get("/api/complaints?page=1&page_size=20")
    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_change_status_allowed_returns_200() -> None:
    client = _client(FakeComplaintService())
    response = client.patch(f"/api/complaints/{OUT.id}/status", json={"status": "in_progress"})
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"


def test_change_status_disallowed_returns_409_verbatim() -> None:
    client = _client(FakeComplaintService())
    response = client.patch(f"/api/complaints/{OUT.id}/status", json={"status": "open"})
    assert response.status_code == 409
    body = response.json()["error"]
    assert body["from_status"] == "resolved"
    assert body["to_status"] == "open"
    assert body["allowed"] == []


def test_rate_limited_create_returns_429_with_retry_after() -> None:
    app = create_app()
    app.dependency_overrides[get_complaint_service] = lambda: FakeComplaintService()

    async def _deny() -> None:
        from app.core.errors import RateLimited

        raise RateLimited(retry_after_s=42)

    app.dependency_overrides[enforce_rate_limit] = _deny
    client = TestClient(app)

    body = {"text": "Burst water main flooding homes", "location": "Street 12"}
    response = client.post("/api/complaints", json=body)
    assert response.status_code == 429
    assert response.headers["Retry-After"] == "42"
    assert response.json()["error"]["code"] == "rate_limited"
