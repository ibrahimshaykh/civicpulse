"""DB-01 acceptance: the model matches plan §9.1's table, verified against the
table's metadata directly (no live database needed) plus a compile check
against the real Postgres dialect for the parts genericized without one."""

from typing import cast

from sqlalchemy import Table
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine import Dialect

from app.db.models import ComplaintORM

TABLE = cast(Table, ComplaintORM.__table__)
# postgresql.dialect is dynamically re-exported, hence the untyped-call ignore.
PG: Dialect = postgresql.dialect()  # type: ignore[no-untyped-call]


def _compiled(column_name: str) -> str:
    return str(TABLE.columns[column_name].type.compile(dialect=PG))


def test_table_name_and_column_set() -> None:
    assert TABLE.name == "complaints"
    assert set(TABLE.columns.keys()) == {
        "id",
        "text",
        "location",
        "reporter_contact",
        "category",
        "priority",
        "status",
        "ai_summary",
        "triaged_by",
        "triage_latency_ms",
        "triage_confidence",
        "created_at",
        "updated_at",
    }


def test_primary_key_is_a_uuid_with_a_server_side_default() -> None:
    assert list(TABLE.primary_key.columns.keys()) == ["id"]
    assert _compiled("id") == "UUID"
    assert TABLE.columns["id"].server_default is not None


def test_enum_columns_compile_to_the_named_postgres_types() -> None:
    assert _compiled("category") == "complaint_category"
    assert _compiled("priority") == "complaint_priority"
    assert _compiled("status") == "complaint_status"


def test_create_table_ddl_never_emits_create_type() -> None:
    """The migration owns CREATE TYPE (plan §9.4). CreateTable alone never emits
    it regardless of the enum's create_type flag -- that only fires via
    metadata.create_all(), which app code never calls (see the test below)."""
    from sqlalchemy.schema import CreateTable

    ddl = str(CreateTable(TABLE).compile(dialect=PG))
    assert "CREATE TYPE" not in ddl


def test_status_defaults_to_open() -> None:
    assert TABLE.columns["status"].server_default.arg == "open"  # type: ignore[union-attr]


def test_timestamps_are_timezone_aware_and_default_to_now() -> None:
    for name in ("created_at", "updated_at"):
        assert _compiled(name) == "TIMESTAMP WITH TIME ZONE"
        assert TABLE.columns[name].nullable is False
        assert TABLE.columns[name].server_default is not None


def test_varchar_lengths_match_the_brief() -> None:
    assert _compiled("location") == "VARCHAR(200)"
    assert _compiled("reporter_contact") == "VARCHAR(120)"
    assert _compiled("ai_summary") == "VARCHAR(140)"
    assert _compiled("triaged_by") == "VARCHAR(32)"
    assert _compiled("text") == "TEXT"


def test_triage_confidence_is_numeric_4_3() -> None:
    assert _compiled("triage_confidence") == "NUMERIC(4, 3)"
    assert TABLE.columns["triage_confidence"].nullable is True


def test_check_constraints_have_deterministic_names() -> None:
    names = {c.name for c in TABLE.constraints if type(c).__name__ == "CheckConstraint"}
    assert names == {
        "ck_complaints_text_length",
        "ck_complaints_location_length",
        "ck_complaints_summary_length",
        "ck_complaints_triaged_by_known",
        "ck_complaints_latency_nonneg",
        "ck_complaints_confidence_range",
    }


def test_indexes_serve_the_dashboard_queries() -> None:
    by_name = {str(i.name): i for i in TABLE.indexes}
    assert set(by_name) == {"ix_complaints_status_priority", "ix_complaints_created_at"}
    assert [c.name for c in by_name["ix_complaints_status_priority"].columns] == ["status", "priority"]
    # A DESC index expression isn't a plain Column, so it isn't in .columns;
    # the plan's own §9.1 calls this index "(created_at DESC)".
    assert [str(e) for e in by_name["ix_complaints_created_at"].expressions] == ["created_at DESC"]


def test_no_create_all_or_raw_create_table_in_app_code() -> None:
    """The migration is the only thing allowed to create the schema (plan §9.4)."""
    import pathlib

    app_dir = pathlib.Path(__file__).resolve().parents[2] / "app"
    for path in app_dir.rglob("*.py"):
        src = path.read_text(encoding="utf-8")
        assert "create_all" not in src, f"{path} calls create_all()"
        assert "create table" not in src.lower(), f"{path} has a raw CREATE TABLE"
