"""Fixture data for the C0-05 stub routes.

Temporary: BE-03, BE-05 and the cache/triage tasks replace every use of this module
with real services. Reading from tests/fixtures keeps one copy of each example
payload (plan §7.4), shared with the unit tests and the frontend's MSW handlers.
"""

import json
from functools import cache
from pathlib import Path
from typing import Any

from app.schemas import ComplaintOut, ProvidersOut, StatsOut

FIXTURES = Path(__file__).resolve().parents[2] / "tests" / "fixtures"


@cache
def _load(name: str) -> Any:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def complaint() -> ComplaintOut:
    return ComplaintOut.model_validate(_load("complaint_201.json"))


def stats() -> StatsOut:
    return StatsOut.model_validate(_load("stats_200.json"))


def providers() -> ProvidersOut:
    return ProvidersOut.model_validate(_load("providers_200.json"))
