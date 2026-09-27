"""What repositories return -- never the ORM object itself. Services build on
this, never on app.db, so an ORM lazy-load can never fire outside a session
(plan §10.6's layering detail)."""

import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from app.domain.enums import Category, Priority, Status


@dataclass(frozen=True, slots=True)
class ComplaintRecord:
    id: uuid.UUID
    text: str
    location: str
    reporter_contact: str | None
    category: Category
    priority: Priority
    status: Status
    ai_summary: str | None
    triaged_by: str
    triage_latency_ms: int
    triage_confidence: Decimal | None
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class StatsAggregate:
    """What ComplaintRepository.aggregate() returns -- not StatsOut itself, so
    the repository never imports app.schemas (a presentation-layer package),
    matching the same records-not-schemas split as ComplaintRecord. The
    service layer adds generated_at and returns the real StatsOut.
    """

    total: int
    by_category: dict[Category, int]
    by_priority: dict[Priority, int]
    by_status: dict[Status, int]
