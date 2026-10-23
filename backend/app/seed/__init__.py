"""Idempotent seed data (plan §9.5). Every row has a stable slug; its UUID is
uuid5(SEED_NAMESPACE, slug), so it is the same on every run and every machine.
The insert is ON CONFLICT DO NOTHING, so running the seed twice inserts 0 rows
the second time -- no TRUNCATE, no "delete and reinsert" that would also wipe
any real complaints an operator has since resolved.

The seed never calls an LLM: triaged_by is always "rules" and
triage_latency_ms is 0, so a stranger's first `up` costs zero API quota.
"""

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Protocol

from app.domain.enums import Category, Priority, Status

SEED_NAMESPACE = uuid.UUID("6f3b0c1e-2b8a-4f9e-9d2c-5a1e7c3b9f00")
SEED_FILE = Path(__file__).resolve().parent / "complaints.json"


@dataclass(frozen=True, slots=True)
class SeedRow:
    slug: str
    category: Category
    priority: Priority
    status: Status
    days_ago: int
    text: str
    location: str
    summary: str
    hour_offset: int = 0


@dataclass(frozen=True, slots=True)
class SeedReport:
    inserted: int
    skipped: int


class SeedRepository(Protocol):
    """What seed() needs from a repository -- ComplaintRepository.insert_if_absent
    satisfies this; tests use a lightweight fake instead of a real database."""

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
    ) -> bool: ...


def load_seed_rows(path: Path = SEED_FILE) -> list[SeedRow]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [
        SeedRow(
            slug=r["slug"],
            category=Category(r["category"]),
            priority=Priority(r["priority"]),
            status=Status(r["status"]),
            days_ago=r["days_ago"],
            text=r["text"],
            location=r["location"],
            summary=r["summary"],
            hour_offset=r.get("hour_offset", 0),
        )
        for r in raw
    ]


async def seed(repo: SeedRepository, rows: list[SeedRow], now: datetime) -> SeedReport:
    inserted = 0
    for r in rows:
        ok = await repo.insert_if_absent(
            id=uuid.uuid5(SEED_NAMESPACE, r.slug),
            text=r.text,
            location=r.location,
            reporter_contact=None,
            category=r.category,
            priority=r.priority,
            status=r.status,
            ai_summary=r.summary,
            triaged_by="rules",
            triage_latency_ms=0,
            triage_confidence=None,
            created_at=now - timedelta(days=r.days_ago, hours=r.hour_offset),
        )
        inserted += int(ok)
    return SeedReport(inserted=inserted, skipped=len(rows) - inserted)
