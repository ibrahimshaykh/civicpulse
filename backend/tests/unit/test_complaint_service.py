"""BE-03/BE-04 acceptance: ComplaintService against fakes, no database.
Repository-level optimistic concurrency (update_status_if) is already
covered by test_complaint_repository.py; this proves the service turns a
lost race into the correct 409, not the SQL itself.
"""

from dataclasses import replace
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

import pytest

from app.core.errors import InvalidTransition, NotFound
from app.domain.enums import Category, Priority, Status
from app.domain.records import ComplaintRecord
from app.providers.triage.base import TriageResult
from app.schemas import ComplaintCreate
from app.services.complaint_service import ComplaintQuery, ComplaintService
from app.services.triage_service import TriageOutcome

NOW = datetime(2026, 1, 1, tzinfo=UTC)


def _record(**overrides: object) -> ComplaintRecord:
    base = ComplaintRecord(
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
        created_at=NOW,
        updated_at=NOW,
    )
    return replace(base, **overrides)  # type: ignore[arg-type]


class FakeRepo:
    def __init__(self, rows: dict[UUID, ComplaintRecord] | None = None) -> None:
        self.rows = rows or {}
        self.inserted: list[dict[str, object]] = []

    async def insert(self, **fields: object) -> ComplaintRecord:
        self.inserted.append(fields)
        row = _record(**{k: v for k, v in fields.items() if k != "id"}, id=fields["id"])
        self.rows[row.id] = row
        return row

    async def get(self, id: UUID) -> ComplaintRecord | None:
        return self.rows.get(id)

    async def get_status(self, id: UUID) -> Status | None:
        row = self.rows.get(id)
        return row.status if row else None

    async def list_page(
        self, category: object, priority: object, status: object, page: int, page_size: int
    ) -> tuple[list[ComplaintRecord], int]:
        rows = list(self.rows.values())
        return rows[(page - 1) * page_size : page * page_size], len(rows)

    async def update_status_if(self, id: UUID, *, expected: Status, target: Status) -> ComplaintRecord | None:
        row = self.rows.get(id)
        if row is None or row.status != expected:
            return None
        updated = replace(row, status=target)
        self.rows[id] = updated
        return updated


class FakeUoW:
    def __init__(self) -> None:
        self.commits = 0

    async def commit(self) -> None:
        self.commits += 1

    async def rollback(self) -> None:
        pass


class FakeStatsCache:
    def __init__(self) -> None:
        self.invalidated = 0

    async def invalidate(self) -> None:
        self.invalidated += 1


class FixedTriageService:
    active_provider = "rules"

    def __init__(self, result: TriageResult) -> None:
        self._result = result

    async def triage(self, *, complaint_id: UUID, text: str, location: str) -> TriageOutcome:
        return TriageOutcome(self._result, "rules", 1, cache_hit=False, fallback=False, error_class=None)


RESULT = TriageResult(category=Category.water, priority=Priority.high, summary="Burst main", confidence=0.9)


def _service(repo: FakeRepo | None = None) -> tuple[ComplaintService, FakeRepo, FakeUoW, FakeStatsCache]:
    repo = repo or FakeRepo()
    uow = FakeUoW()
    cache = FakeStatsCache()
    svc = ComplaintService(repo, uow, FixedTriageService(RESULT), cache)  # type: ignore[arg-type]
    return svc, repo, uow, cache


async def test_create_triages_persists_and_invalidates_stats() -> None:
    svc, repo, uow, cache = _service()
    out = await svc.create(ComplaintCreate(text="Burst water main flooding homes", location="Street 12"))

    assert out.category == Category.water
    assert out.priority == Priority.high
    assert out.allowed_transitions == [Status.in_progress, Status.rejected]
    assert uow.commits == 1
    assert cache.invalidated == 1
    assert len(repo.inserted) == 1


async def test_get_missing_complaint_raises_not_found() -> None:
    svc, _, _, _ = _service()
    with pytest.raises(NotFound):
        await svc.get(uuid4())


async def test_list_paginates() -> None:
    repo = FakeRepo({r.id: r for r in (_record(id=uuid4()), _record(id=uuid4()), _record(id=uuid4()))})
    svc, _, _, _ = _service(repo)
    page = await svc.list(ComplaintQuery(category=None, priority=None, status=None, page=1, page_size=2))
    assert page.total == 3
    assert page.pages == 2
    assert len(page.items) == 2


async def test_change_status_allowed_transition_commits_and_invalidates() -> None:
    row = _record(status=Status.open)
    repo = FakeRepo({row.id: row})
    svc, _, uow, cache = _service(repo)

    out = await svc.change_status(row.id, Status.in_progress)

    assert out.status == Status.in_progress
    assert out.allowed_transitions == [Status.resolved, Status.rejected]
    assert uow.commits == 1
    assert cache.invalidated == 1


async def test_change_status_missing_complaint_raises_not_found() -> None:
    svc, _, _, _ = _service()
    with pytest.raises(NotFound):
        await svc.change_status(uuid4(), Status.in_progress)


async def test_change_status_disallowed_transition_raises_409_with_allowed_list() -> None:
    row = _record(status=Status.resolved)
    repo = FakeRepo({row.id: row})
    svc, _, _, _ = _service(repo)

    with pytest.raises(InvalidTransition) as exc_info:
        await svc.change_status(row.id, Status.open)

    assert exc_info.value.allowed == []  # resolved is terminal


async def test_change_status_lost_race_raises_409_with_the_real_current_status() -> None:
    """Simulates two operators racing: repo.update_status_if returns None as
    if another writer already moved the row past what this caller expected."""
    row = _record(status=Status.in_progress)  # what the caller *thinks* is current

    class RacingRepo(FakeRepo):
        async def get_status(self, id: UUID) -> Status | None:
            # First call (pre-check) sees in_progress; second call (post-race
            # recheck) sees what "actually" won the race: resolved.
            self.calls = getattr(self, "calls", 0) + 1
            return Status.in_progress if self.calls == 1 else Status.resolved

        async def update_status_if(
            self, id: UUID, *, expected: Status, target: Status
        ) -> ComplaintRecord | None:
            return None  # someone else already changed it

    racing = RacingRepo({row.id: row})
    svc, _, _, _ = _service(racing)

    with pytest.raises(InvalidTransition) as exc_info:
        await svc.change_status(row.id, Status.rejected)

    assert exc_info.value.current == Status.resolved
