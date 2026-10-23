import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, Index, Integer, Numeric, String, Text, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy import text as sql_text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.domain.enums import Category, Priority, Status


def pg_enum(enum_cls: type, name: str) -> SAEnum:
    # native_enum + create_type=False: the migration owns creating the PG enum
    # type, so an autogenerate diff never tries to CREATE TYPE a second time.
    return SAEnum(
        enum_cls,
        name=name,
        values_callable=lambda e: [m.value for m in e],
        native_enum=True,
        create_type=False,
    )


class ComplaintORM(Base):
    __tablename__ = "complaints"

    id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=sql_text("gen_random_uuid()")
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[str] = mapped_column(String(200), nullable=False)
    reporter_contact: Mapped[str | None] = mapped_column(String(120))
    category: Mapped[Category] = mapped_column(pg_enum(Category, "complaint_category"), nullable=False)
    priority: Mapped[Priority] = mapped_column(pg_enum(Priority, "complaint_priority"), nullable=False)
    status: Mapped[Status] = mapped_column(
        pg_enum(Status, "complaint_status"), nullable=False, server_default="open"
    )
    ai_summary: Mapped[str | None] = mapped_column(String(140))
    triaged_by: Mapped[str] = mapped_column(String(32), nullable=False)
    triage_latency_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    triage_confidence: Mapped[Decimal | None] = mapped_column(Numeric(4, 3))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("char_length(text) BETWEEN 10 AND 2000", name="text_length"),
        CheckConstraint("char_length(location) BETWEEN 3 AND 200", name="location_length"),
        CheckConstraint("ai_summary IS NULL OR char_length(ai_summary) <= 140", name="summary_length"),
        CheckConstraint(
            "triaged_by IN ('llm:groq','llm:ollama','rules','rules:fallback','simulated')",
            name="triaged_by_known",
        ),
        CheckConstraint("triage_latency_ms >= 0", name="latency_nonneg"),
        CheckConstraint(
            "triage_confidence IS NULL OR triage_confidence BETWEEN 0 AND 1", name="confidence_range"
        ),
        Index("ix_complaints_status_priority", "status", "priority"),
        Index("ix_complaints_created_at", sql_text("created_at DESC")),
    )
