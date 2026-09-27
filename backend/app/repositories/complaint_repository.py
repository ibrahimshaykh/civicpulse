"""SQL lives here and in app/db only (ruff's banned-api rule enforces this
everywhere else). BE-02 extends this class with get/list/update_status; for
now it has only what DB-03's seed CLI needs.
"""

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.dml import ReturningInsert

from app.db.models import ComplaintORM
from app.domain.enums import Category, Priority, Status


def insert_if_absent_stmt(
    *,
    id: uuid.UUID,
    text: str,
    location: str,
    reporter_contact: str | None,
    category: Category,
    priority: Priority,
    status: Status,
    ai_summary: str | None,
    triaged_by: str,
    triage_latency_ms: int,
    triage_confidence: Decimal | None,
    created_at: datetime,
) -> ReturningInsert[tuple[uuid.UUID]]:
    """Pure statement builder, kept apart from execution so its SQL can be
    compiled and checked in a test without a database connection."""
    return (
        pg_insert(ComplaintORM)
        .values(
            id=id,
            text=text,
            location=location,
            reporter_contact=reporter_contact,
            category=category,
            priority=priority,
            status=status,
            ai_summary=ai_summary,
            triaged_by=triaged_by,
            triage_latency_ms=triage_latency_ms,
            triage_confidence=triage_confidence,
            created_at=created_at,
            updated_at=created_at,
        )
        .on_conflict_do_nothing(index_elements=["id"])
        .returning(ComplaintORM.id)
    )


class ComplaintRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert_if_absent(
        self,
        *,
        id: uuid.UUID,
        text: str,
        location: str,
        reporter_contact: str | None,
        category: Category,
        priority: Priority,
        status: Status,
        ai_summary: str | None,
        triaged_by: str,
        triage_latency_ms: int,
        triage_confidence: Decimal | None,
        created_at: datetime,
    ) -> bool:
        """Returns True if a row was actually inserted, False if `id` already
        existed (ON CONFLICT DO NOTHING) -- the mechanism the seed CLI's
        idempotency relies on: running it twice inserts 0 rows the second time.
        """
        stmt = insert_if_absent_stmt(
            id=id,
            text=text,
            location=location,
            reporter_contact=reporter_contact,
            category=category,
            priority=priority,
            status=status,
            ai_summary=ai_summary,
            triaged_by=triaged_by,
            triage_latency_ms=triage_latency_ms,
            triage_confidence=triage_confidence,
            created_at=created_at,
        )
        result = await self._session.execute(stmt)
        return result.first() is not None
