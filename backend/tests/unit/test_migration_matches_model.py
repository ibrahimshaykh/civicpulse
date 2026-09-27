"""DB-02 acceptance (partial): the migration and the ORM model agree.

`alembic check` (plan §9.4) needs a live Postgres to reflect the actual schema
and compare it against the model -- unavailable in this sandbox (no Docker, no
local Postgres). As a proxy, this generates the migration's DDL offline
(`alembic upgrade head --sql`, which needs no DBAPI or connection at all) and
diffs its CREATE TABLE against the one SQLAlchemy compiles directly from
`ComplaintORM`. A version-2 migration that changes a column without updating
the ORM model (or vice versa) fails this test immediately.

This is not a substitute for I21 (`upgrade head -> downgrade base -> upgrade
head` against a real container) -- that still has to run once Docker exists.
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import cast

from sqlalchemy import Table
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateTable

from app.db.models import ComplaintORM

BACKEND = Path(__file__).resolve().parents[2]


def _normalize(ddl: str) -> str:
    return re.sub(r"\s+", " ", ddl).strip().rstrip(";")


def _model_create_table_sql() -> str:
    table = cast(Table, ComplaintORM.__table__)
    # postgresql.dialect is dynamically re-exported, hence the untyped-call ignore.
    dialect = postgresql.dialect()  # type: ignore[no-untyped-call]
    return _normalize(str(CreateTable(table).compile(dialect=dialect)))


def _migration_create_table_sql() -> str:
    env = {**os.environ, "POSTGRES_PASSWORD": "x", "REDIS_PASSWORD": "y"}
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head", "--sql"],
        cwd=BACKEND,
        capture_output=True,
        text=True,
        env=env,
        check=True,
    )
    match = re.search(r"CREATE TABLE complaints \(.*?\);", result.stdout, re.DOTALL)
    assert match, f"no CREATE TABLE complaints found in:\n{result.stdout}"
    return _normalize(match.group(0))


def test_migration_ddl_matches_the_orm_model() -> None:
    assert _migration_create_table_sql() == _model_create_table_sql()
