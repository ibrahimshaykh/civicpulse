"""Repository SQL, checked by compiling it against the real Postgres dialect --
no database connection needed. A live INSERT ... ON CONFLICT round-trip still
needs Docker/Postgres."""

import uuid
from datetime import datetime

from sqlalchemy.dialects import postgresql

from app.repositories.complaint_repository import insert_if_absent_stmt


def _compiled_sql() -> str:
    stmt = insert_if_absent_stmt(
        id=uuid.uuid4(),
        text="A" * 20,
        location="Somewhere",
        reporter_contact=None,
        category="water",  # type: ignore[arg-type]
        priority="high",  # type: ignore[arg-type]
        status="open",  # type: ignore[arg-type]
        ai_summary=None,
        triaged_by="rules",
        triage_latency_ms=0,
        triage_confidence=None,
        created_at=datetime(2026, 1, 1),
    )
    return str(stmt.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": False}))  # type: ignore[no-untyped-call]


def test_statement_targets_the_complaints_table() -> None:
    assert "INSERT INTO complaints" in _compiled_sql()


def test_statement_is_on_conflict_do_nothing_on_id() -> None:
    sql = _compiled_sql()
    assert "ON CONFLICT (id) DO NOTHING" in sql


def test_statement_returns_id_so_the_caller_can_tell_insert_from_skip() -> None:
    assert "RETURNING complaints.id" in _compiled_sql()
