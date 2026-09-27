from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from app.domain.enums import Category, Priority, Status

ComplaintText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=10, max_length=2000)]
LocationText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=200)]
ContactText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=120)]


class ComplaintCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: ComplaintText
    location: LocationText
    reporter_contact: ContactText | None = None


class ComplaintOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    text: str
    location: str
    reporter_contact: str | None
    category: Category
    priority: Priority
    status: Status
    ai_summary: str | None = Field(default=None, max_length=140)
    triaged_by: str
    triage_latency_ms: int
    triage_confidence: float | None
    created_at: datetime
    updated_at: datetime
    # Computed by the service from the TRANSITIONS table; the frontend never holds its own copy.
    allowed_transitions: list[Status]


class ComplaintPage(BaseModel):
    items: list[ComplaintOut]
    total: int
    page: int
    page_size: int
    pages: int


class StatusUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Status
