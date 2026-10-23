"""create complaints

Revision ID: 0001
Revises:
Create Date: 2026-09-27

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None

CATEGORY = postgresql.ENUM(
    "water", "electricity", "sanitation", "roads", "streetlights", "other", name="complaint_category"
)
PRIORITY = postgresql.ENUM("high", "normal", "low", name="complaint_priority")
STATUS = postgresql.ENUM("open", "in_progress", "resolved", "rejected", name="complaint_status")


def upgrade() -> None:
    bind = op.get_bind()
    for e in (CATEGORY, PRIORITY, STATUS):
        e.create(bind, checkfirst=True)

    op.create_table(
        "complaints",
        sa.Column(
            "id", postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")
        ),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("location", sa.String(200), nullable=False),
        sa.Column("reporter_contact", sa.String(120)),
        sa.Column("category", postgresql.ENUM(name="complaint_category", create_type=False), nullable=False),
        sa.Column("priority", postgresql.ENUM(name="complaint_priority", create_type=False), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM(name="complaint_status", create_type=False),
            nullable=False,
            server_default="open",
        ),
        sa.Column("ai_summary", sa.String(140)),
        sa.Column("triaged_by", sa.String(32), nullable=False),
        sa.Column("triage_latency_ms", sa.Integer(), nullable=False),
        sa.Column("triage_confidence", sa.Numeric(4, 3)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint("char_length(text) BETWEEN 10 AND 2000", name="text_length"),
        sa.CheckConstraint("char_length(location) BETWEEN 3 AND 200", name="location_length"),
        sa.CheckConstraint("ai_summary IS NULL OR char_length(ai_summary) <= 140", name="summary_length"),
        sa.CheckConstraint(
            "triaged_by IN ('llm:groq','llm:ollama','rules','rules:fallback','simulated')",
            name="triaged_by_known",
        ),
        sa.CheckConstraint("triage_latency_ms >= 0", name="latency_nonneg"),
        sa.CheckConstraint(
            "triage_confidence IS NULL OR triage_confidence BETWEEN 0 AND 1",
            name="confidence_range",
        ),
    )
    op.create_index("ix_complaints_status_priority", "complaints", ["status", "priority"])
    op.create_index("ix_complaints_created_at", "complaints", [sa.text("created_at DESC")])

    # Trigger, not application code: even a manual psql UPDATE maintains updated_at.
    op.execute("""
        CREATE FUNCTION set_updated_at() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN NEW.updated_at = now(); RETURN NEW; END; $$;
    """)
    op.execute("""
        CREATE TRIGGER trg_complaints_updated_at BEFORE UPDATE ON complaints
        FOR EACH ROW EXECUTE FUNCTION set_updated_at();
    """)


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS trg_complaints_updated_at ON complaints")
    op.execute("DROP FUNCTION IF EXISTS set_updated_at()")
    op.drop_index("ix_complaints_created_at", table_name="complaints")
    op.drop_index("ix_complaints_status_priority", table_name="complaints")
    op.drop_table("complaints")
    bind = op.get_bind()
    for e in (STATUS, PRIORITY, CATEGORY):
        e.drop(bind, checkfirst=True)
