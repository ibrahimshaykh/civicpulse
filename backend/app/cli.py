"""Command-line entry points: ``uv run python -m app.cli <command>``."""

import argparse
import asyncio
import json
import sys
from datetime import UTC, datetime

import structlog

from app.core.config import Settings
from app.core.logging import configure_logging
from app.db.session import build_engine, build_sessionmaker
from app.main import create_app
from app.repositories.complaint_repository import ComplaintRepository
from app.seed import load_seed_rows, seed

log = structlog.get_logger()


def export_openapi() -> None:
    schema = create_app().openapi()
    # LF on every OS, so the committed file is identical whether it was exported on Windows or in CI.
    sys.stdout.reconfigure(newline="\n", encoding="utf-8")  # type: ignore[union-attr]
    sys.stdout.write(json.dumps(schema, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


async def _run_seed() -> None:
    settings = Settings()
    configure_logging(settings.log_level)
    engine = build_engine(settings)
    sessionmaker = build_sessionmaker(engine)
    rows = load_seed_rows()
    async with sessionmaker() as session, session.begin():
        repo = ComplaintRepository(session)
        report = await seed(repo, rows, now=datetime.now(UTC))
    await engine.dispose()
    log.info("seed_complete", inserted=report.inserted, skipped=report.skipped)


def run_seed() -> None:
    asyncio.run(_run_seed())


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="app.cli")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("export-openapi", help="print the OpenAPI schema as sorted JSON")
    sub.add_parser("seed", help="idempotently load the 33 seed complaints")
    args = parser.parse_args(argv)
    if args.command == "export-openapi":
        export_openapi()
    elif args.command == "seed":
        run_seed()


if __name__ == "__main__":
    main()
