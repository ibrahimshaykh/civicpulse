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
