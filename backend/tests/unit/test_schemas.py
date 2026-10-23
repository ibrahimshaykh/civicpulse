import json
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from app.domain.enums import Category, Priority, Status
from app.schemas import ComplaintCreate, ComplaintOut, ComplaintPage, ErrorBody, StatsOut, StatusUpdate

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures"


def load(name: str) -> Any:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_create_accepts_the_example_request() -> None:
    body = ComplaintCreate.model_validate(load("complaint_create.json"))
    assert body.location == "Street 12, G-9/2, Islamabad"


def test_create_strips_whitespace_before_length_check() -> None:
    with pytest.raises(ValidationError) as exc:
        ComplaintCreate(text="   too short   ", location="G-9")
    assert exc.value.errors()[0]["type"] == "string_too_short"
    assert exc.value.errors()[0]["loc"] == ("text",)


def test_create_rejects_unknown_fields() -> None:
    # Clients can't set category/priority themselves; triage decides those.
    with pytest.raises(ValidationError) as exc:
        ComplaintCreate.model_validate({**load("complaint_create.json"), "priority": "high"})
    assert exc.value.errors()[0]["type"] == "extra_forbidden"


def test_create_contact_is_optional() -> None:
    assert ComplaintCreate(text="Streetlight out for a week", location="F-7").reporter_contact is None


@pytest.mark.parametrize(
    ("field", "value"),
    [("text", "x" * 2001), ("location", "ab"), ("reporter_contact", "x" * 121)],
)
def test_create_enforces_length_limits(field: str, value: str) -> None:
    with pytest.raises(ValidationError):
        ComplaintCreate.model_validate({**load("complaint_create.json"), field: value})


def test_complaint_out_round_trips_the_example_response() -> None:
    out = ComplaintOut.model_validate(load("complaint_201.json"))
    assert out.category is Category.water
    assert out.priority is Priority.high
    assert out.allowed_transitions == [Status.in_progress, Status.rejected]
    dumped = out.model_dump(mode="json")
    assert dumped["category"] == "water"
    assert dumped["allowed_transitions"] == ["in_progress", "rejected"]


def test_complaint_out_rejects_long_summary() -> None:
    with pytest.raises(ValidationError):
        ComplaintOut.model_validate({**load("complaint_201.json"), "ai_summary": "x" * 141})


def test_page_wraps_items() -> None:
    item = ComplaintOut.model_validate(load("complaint_201.json"))
    page = ComplaintPage(items=[item], total=1, page=1, page_size=20, pages=1)
    assert page.items[0].status is Status.open


def test_status_update_rejects_unknown_status() -> None:
    with pytest.raises(ValidationError) as exc:
        StatusUpdate.model_validate({"status": "closed"})
    assert exc.value.errors()[0]["type"] == "enum"


def test_stats_keys_are_enum_values() -> None:
    stats = StatsOut.model_validate(
        {
            "total": 1,
            "by_category": {c.value: int(c is Category.water) for c in Category},
            "by_priority": {p.value: 0 for p in Priority},
            "by_status": {s.value: 0 for s in Status},
            "generated_at": "2026-10-05T04:12:33Z",
        }
    )
    assert stats.by_category[Category.water] == 1
    assert set(stats.model_dump(mode="json")["by_category"]) == {c.value for c in Category}


@pytest.mark.parametrize("name", ["error_400.json", "error_409.json", "error_429.json"])
def test_error_examples_fit_the_envelope(name: str) -> None:
    body = ErrorBody.model_validate(load(name))
    assert body.model_dump(mode="json", exclude_none=True) == load(name)
