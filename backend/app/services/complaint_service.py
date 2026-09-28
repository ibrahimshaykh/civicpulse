"""Complaint use cases (tasks BE-03, BE-04): create, get, list, and the
status state machine. Depends on repositories/providers only through
Protocols (`UnitOfWork`, `TriageService`'s public surface, `StatsCache`),
never on `app.db` or `sqlalchemy` -- enforced by BE-08's architecture test.
"""

from dataclasses import dataclass
from decimal import Decimal
from math import ceil
from uuid import UUID, uuid4

from app.core.errors import InvalidTransition, NotFound
from app.domain.enums import Category, Priority, Status
from app.domain.records import ComplaintRecord
from app.domain.state_machine import allowed_from, is_allowed
from app.providers.cache import StatsCache
from app.repositories.complaint_repository import ComplaintRepository
from app.schemas import ComplaintCreate, ComplaintOut, ComplaintPage
from app.services.triage_service import TriageService
from app.services.uow import UnitOfWork


@dataclass(frozen=True, slots=True)
class ComplaintQuery:
    category: Category | None
    priority: Priority | None
    status: Status | None
    page: int
    page_size: int


class ComplaintService:
    def __init__(
        self, repo: ComplaintRepository, uow: UnitOfWork, triage: TriageService, stats_cache: StatsCache
    ) -> None:
        self._repo = repo
        self._uow = uow
        self._triage = triage
        self._stats_cache = stats_cache

    async def create(self, data: ComplaintCreate) -> ComplaintOut:
        complaint_id = uuid4()  # minted before triage, so a fallback's warning log already has it
        outcome = await self._triage.triage(complaint_id=complaint_id, text=data.text, location=data.location)
        row = await self._repo.insert(
            id=complaint_id,
            text=data.text,
            location=data.location,
            reporter_contact=data.reporter_contact,
            category=outcome.result.category,
            priority=outcome.result.priority,
            ai_summary=outcome.result.summary,
            triaged_by=outcome.triaged_by,
            triage_latency_ms=outcome.latency_ms,
            triage_confidence=Decimal(str(outcome.result.confidence)),
        )
        await self._uow.commit()
        await self._stats_cache.invalidate()  # after commit, never before (plan §10.6)
        return self._to_out(row)

    async def get(self, complaint_id: UUID) -> ComplaintOut:
        row = await self._repo.get(complaint_id)
        if row is None:
            raise NotFound(f"No complaint with id {complaint_id}")
        return self._to_out(row)

    async def list(self, q: ComplaintQuery) -> ComplaintPage:
        rows, total = await self._repo.list_page(q.category, q.priority, q.status, q.page, q.page_size)
        return ComplaintPage(
            items=[self._to_out(r) for r in rows],
            total=total,
            page=q.page,
            page_size=q.page_size,
            pages=max(1, ceil(total / q.page_size)),
        )

    async def change_status(self, complaint_id: UUID, target: Status) -> ComplaintOut:
        current = await self._repo.get_status(complaint_id)
        if current is None:
            raise NotFound(f"No complaint with id {complaint_id}")
        if not is_allowed(current, target):
            raise InvalidTransition(current, target, allowed_from(current))
        row = await self._repo.update_status_if(complaint_id, expected=current, target=target)
        if row is None:  # lost the race: someone else changed it between get_status and update_status_if
            now = await self._repo.get_status(complaint_id)
            assert now is not None  # the row can't vanish; complaints are never deleted
            raise InvalidTransition(now, target, allowed_from(now))
        await self._uow.commit()
        await self._stats_cache.invalidate()
        return self._to_out(row)

    def _to_out(self, row: ComplaintRecord) -> ComplaintOut:
        return ComplaintOut(
            id=row.id,
            text=row.text,
            location=row.location,
            reporter_contact=row.reporter_contact,
            category=row.category,
            priority=row.priority,
            status=row.status,
            ai_summary=row.ai_summary,
            triaged_by=row.triaged_by,
            triage_latency_ms=row.triage_latency_ms,
            triage_confidence=float(row.triage_confidence) if row.triage_confidence is not None else None,
            created_at=row.created_at,
            updated_at=row.updated_at,
            allowed_transitions=allowed_from(row.status),
        )
