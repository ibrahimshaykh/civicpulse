"""SQL lives here and in app/db only (ruff's banned-api rule enforces this
everywhere else). Every method returns a ComplaintRecord (app/domain/records.py),
never the ORM object, so a lazy-load can never fire outside this module.

Statement building is split from execution (`*_stmt` functions vs. the
repository's async methods) so each query's SQL can be compiled and checked in
a test without a database connection.
"""

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Any

from sqlalchemy import ColumnElement, RowMapping, Select, and_, func, insert, select, text, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.dml import ReturningInsert, ReturningUpdate

from app.db.models import ComplaintORM
from app.domain.enums import Category, Priority, Status
from app.domain.records import ComplaintRecord, StatsAggregate


def insert_stmt(
    *,
    id: uuid.UUID,
    text: str,
    location: str,
    reporter_contact: str | None,
    category: Category,
    priority: Priority,
    ai_summary: str | None,
    triaged_by: str,
    triage_latency_ms: int,
    triage_confidence: Decimal | None,
) -> ReturningInsert[Any]:
    return (
        insert(ComplaintORM)
        .values(
            id=id,
            text=text,
            location=location,
            reporter_contact=reporter_contact,
            category=category,
            priority=priority,
            status=Status.open,
            ai_summary=ai_summary,
            triaged_by=triaged_by,
            triage_latency_ms=triage_latency_ms,
            triage_confidence=triage_confidence,
        )
        .returning(ComplaintORM.__table__)
    )


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


def get_stmt(id: uuid.UUID) -> Select[Any]:
    return select(ComplaintORM.__table__).where(ComplaintORM.id == id)


def get_status_stmt(id: uuid.UUID) -> Select[Any]:
    return select(ComplaintORM.status).where(ComplaintORM.id == id)


def _filters(
    category: Category | None, priority: Priority | None, status: Status | None
) -> list[ColumnElement[bool]]:
    conditions: list[ColumnElement[bool]] = []
    if category is not None:
        conditions.append(ComplaintORM.category == category)
    if priority is not None:
        conditions.append(ComplaintORM.priority == priority)
    if status is not None:
        conditions.append(ComplaintORM.status == status)
    return conditions


def list_page_stmt(
    category: Category | None, priority: Priority | None, status: Status | None, page: int, page_size: int
) -> Select[Any]:
    conditions = _filters(category, priority, status)
    stmt = select(ComplaintORM.__table__)
    if conditions:
        stmt = stmt.where(and_(*conditions))
    # id DESC as a tiebreaker: seed rows can share created_at, and without a
    # stable secondary sort, pagination could show or hide a row twice.
    return (
        stmt.order_by(ComplaintORM.created_at.desc(), ComplaintORM.id.desc())
        .limit(page_size)
        .offset((page - 1) * page_size)
    )


def list_count_stmt(
    category: Category | None, priority: Priority | None, status: Status | None
) -> Select[Any]:
    conditions = _filters(category, priority, status)
    stmt = select(func.count()).select_from(ComplaintORM.__table__)
    return stmt.where(and_(*conditions)) if conditions else stmt


def update_status_if_stmt(id: uuid.UUID, *, expected: Status, target: Status) -> ReturningUpdate[Any]:
    """Optimistic concurrency: the WHERE clause requires the row to still be in
    `expected`. Two operators racing on the same complaint cannot both
    succeed -- the loser gets no row back and the service turns that into a
    409 (plan §10.7). updated_at is left to the database trigger, not set here.
    """
    return (
        update(ComplaintORM)
        .where(ComplaintORM.id == id, ComplaintORM.status == expected)
        .values(status=target)
        .returning(ComplaintORM.__table__)
    )


def aggregate_stmt() -> Select[Any]:
    """One query for all three breakdowns plus the grand total, via GROUPING
    SETS -- cheaper than four separate GROUP BY queries (plan §10.6). GROUPING(col)
    is 0 when that grouping set includes col, 1 when col is rolled up (NULL).
    """
    return (
        select(
            ComplaintORM.category,
            ComplaintORM.priority,
            ComplaintORM.status,
            func.count().label("n"),
            func.grouping(ComplaintORM.category).label("g_cat"),
            func.grouping(ComplaintORM.priority).label("g_pri"),
            func.grouping(ComplaintORM.status).label("g_sta"),
        )
        .select_from(ComplaintORM.__table__)
        .group_by(text("GROUPING SETS ((category), (priority), (status), ())"))
    )


def _to_aggregate(rows: list[RowMapping]) -> StatsAggregate:
    total = 0
    by_category: dict[Category, int] = dict.fromkeys(Category, 0)
    by_priority: dict[Priority, int] = dict.fromkeys(Priority, 0)
    by_status: dict[Status, int] = dict.fromkeys(Status, 0)
    for row in rows:
        n = row["n"]
        if row["g_cat"] == 0:
            by_category[row["category"]] = n
        elif row["g_pri"] == 0:
            by_priority[row["priority"]] = n
        elif row["g_sta"] == 0:
            by_status[row["status"]] = n
        else:
            total = n  # the "()" grouping set: the grand total, no columns
    return StatsAggregate(total=total, by_category=by_category, by_priority=by_priority, by_status=by_status)


def _to_record(row: RowMapping) -> ComplaintRecord:
    return ComplaintRecord(
        id=row["id"],
        text=row["text"],
        location=row["location"],
        reporter_contact=row["reporter_contact"],
        category=row["category"],
        priority=row["priority"],
        status=row["status"],
        ai_summary=row["ai_summary"],
        triaged_by=row["triaged_by"],
        triage_latency_ms=row["triage_latency_ms"],
        triage_confidence=row["triage_confidence"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


class ComplaintRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def insert(
        self,
        *,
        id: uuid.UUID,
        text: str,
        location: str,
        reporter_contact: str | None,
        category: Category,
        priority: Priority,
        ai_summary: str | None,
        triaged_by: str,
        triage_latency_ms: int,
        triage_confidence: Decimal | None,
    ) -> ComplaintRecord:
        stmt = insert_stmt(
            id=id,
            text=text,
            location=location,
            reporter_contact=reporter_contact,
            category=category,
            priority=priority,
            ai_summary=ai_summary,
            triaged_by=triaged_by,
            triage_latency_ms=triage_latency_ms,
            triage_confidence=triage_confidence,
        )
        result = await self._session.execute(stmt)
        return _to_record(result.mappings().one())

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

    async def get(self, id: uuid.UUID) -> ComplaintRecord | None:
        row = (await self._session.execute(get_stmt(id))).mappings().first()
        return _to_record(row) if row is not None else None

    async def get_status(self, id: uuid.UUID) -> Status | None:
        return (await self._session.execute(get_status_stmt(id))).scalar_one_or_none()

    async def list_page(
        self,
        category: Category | None,
        priority: Priority | None,
        status: Status | None,
        page: int,
        page_size: int,
    ) -> tuple[list[ComplaintRecord], int]:
        rows = (
            (await self._session.execute(list_page_stmt(category, priority, status, page, page_size)))
            .mappings()
            .all()
        )
        total = (await self._session.execute(list_count_stmt(category, priority, status))).scalar_one()
        return [_to_record(r) for r in rows], total

    async def update_status_if(
        self, id: uuid.UUID, *, expected: Status, target: Status
    ) -> ComplaintRecord | None:
        row = (
            (await self._session.execute(update_status_if_stmt(id, expected=expected, target=target)))
            .mappings()
            .first()
        )
        return _to_record(row) if row is not None else None

    async def aggregate(self) -> StatsAggregate:
        rows = (await self._session.execute(aggregate_stmt())).mappings().all()
        return _to_aggregate(list(rows))
