"""Repository SQL, checked by compiling it against the real Postgres dialect --
no database connection needed. A live round-trip against Postgres still needs
Docker (see test_migration_matches_model.py's docstring for the same gap)."""

import uuid
from datetime import datetime

from sqlalchemy.dialects import postgresql

from app.domain.records import ComplaintRecord
from app.repositories.complaint_repository import (
    _to_record,
    get_status_stmt,
    get_stmt,
    insert_if_absent_stmt,
    insert_stmt,
    list_count_stmt,
    list_page_stmt,
    update_status_if_stmt,
)

# postgresql.dialect is dynamically re-exported, hence the untyped-call ignore.
PG = postgresql.dialect()  # type: ignore[no-untyped-call]


def _sql(stmt: object) -> str:
    return str(stmt.compile(dialect=PG, compile_kwargs={"literal_binds": True}))  # type: ignore[attr-defined]


def _insert_if_absent_sql() -> str:
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
    return _sql(stmt)


def test_insert_if_absent_targets_the_complaints_table() -> None:
    assert "INSERT INTO complaints" in _insert_if_absent_sql()


def test_insert_if_absent_is_on_conflict_do_nothing_on_id() -> None:
    assert "ON CONFLICT (id) DO NOTHING" in _insert_if_absent_sql()


def test_insert_if_absent_returns_id_so_the_caller_can_tell_insert_from_skip() -> None:
    assert "RETURNING complaints.id" in _insert_if_absent_sql()


def test_insert_stmt_starts_new_complaints_as_open() -> None:
    stmt = insert_stmt(
        id=uuid.uuid4(),
        text="A" * 20,
        location="Somewhere",
        reporter_contact=None,
        category="water",  # type: ignore[arg-type]
        priority="high",  # type: ignore[arg-type]
        ai_summary=None,
        triaged_by="llm:groq",
        triage_latency_ms=400,
        triage_confidence=None,
    )
    sql = _sql(stmt)
    assert "INSERT INTO complaints" in sql
    assert "'open'" in sql
    assert "RETURNING complaints." in sql


def test_get_stmt_filters_by_id() -> None:
    id_ = uuid.uuid4()
    sql = _sql(get_stmt(id_))
    assert "SELECT complaints." in sql
    assert f"WHERE complaints.id = '{id_}'" in sql


def test_get_status_stmt_selects_only_the_status_column() -> None:
    id_ = uuid.uuid4()
    sql = _sql(get_status_stmt(id_))
    assert sql.startswith("SELECT complaints.status")
    assert "complaints.text" not in sql


def test_list_page_stmt_with_no_filters_orders_and_paginates() -> None:
    sql = _sql(list_page_stmt(None, None, None, page=1, page_size=20))
    assert "WHERE" not in sql
    assert "ORDER BY complaints.created_at DESC, complaints.id DESC" in sql
    assert "LIMIT 20" in sql
    assert "OFFSET 0" in sql


def test_list_page_stmt_page_two_offsets_by_page_size() -> None:
    sql = _sql(list_page_stmt(None, None, None, page=2, page_size=20))
    assert "OFFSET 20" in sql


def test_list_page_stmt_combines_filters() -> None:
    sql = _sql(list_page_stmt("water", "high", "open", page=1, page_size=20))  # type: ignore[arg-type]
    assert "complaints.category = 'water'" in sql
    assert "complaints.priority = 'high'" in sql
    assert "complaints.status = 'open'" in sql
    assert " AND " in sql


def test_list_count_stmt_has_no_limit_or_order() -> None:
    sql = _sql(list_count_stmt("water", None, None))  # type: ignore[arg-type]
    assert "count(*)" in sql.lower()
    assert "LIMIT" not in sql
    assert "ORDER BY" not in sql


def test_update_status_if_stmt_requires_the_expected_current_status() -> None:
    id_ = uuid.uuid4()
    sql = _sql(update_status_if_stmt(id_, expected="open", target="in_progress"))  # type: ignore[arg-type]
    assert "UPDATE complaints SET status='in_progress'" in sql
    assert f"complaints.id = '{id_}'" in sql
    assert "complaints.status = 'open'" in sql
    assert "RETURNING complaints." in sql


def test_to_record_maps_every_field_by_name() -> None:
    id_ = uuid.uuid4()
    now = datetime(2026, 1, 1, 12, 0, 0)
    row = {
        "id": id_,
        "text": "Something is wrong here",
        "location": "Street 1",
        "reporter_contact": None,
        "category": "water",
        "priority": "high",
        "status": "open",
        "ai_summary": None,
        "triaged_by": "rules",
        "triage_latency_ms": 0,
        "triage_confidence": None,
        "created_at": now,
        "updated_at": now,
    }
    record = _to_record(row)  # type: ignore[arg-type]
    assert record == ComplaintRecord(
        id=id_,
        text="Something is wrong here",
        location="Street 1",
        reporter_contact=None,
        category="water",  # type: ignore[arg-type]
        priority="high",  # type: ignore[arg-type]
        status="open",  # type: ignore[arg-type]
        ai_summary=None,
        triaged_by="rules",
        triage_latency_ms=0,
        triage_confidence=None,
        created_at=now,
        updated_at=now,
    )
