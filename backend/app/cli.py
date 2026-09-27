"""Command-line entry points: ``uv run python -m app.cli <command>``."""

import argparse
import json
import sys

from app.main import create_app


def export_openapi() -> None:
    schema = create_app().openapi()
    # LF on every OS, so the committed file is identical whether it was exported on Windows or in CI.
    sys.stdout.reconfigure(newline="\n", encoding="utf-8")  # type: ignore[union-attr]
    sys.stdout.write(json.dumps(schema, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="app.cli")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("export-openapi", help="print the OpenAPI schema as sorted JSON")
    args = parser.parse_args(argv)
    if args.command == "export-openapi":
        export_openapi()


if __name__ == "__main__":
    main()
