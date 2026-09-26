import json

from app.domain.enums import Category, Priority, Status, TriagedBy


def test_enum_values_match_the_brief() -> None:
    assert [c.value for c in Category] == [
        "water",
        "electricity",
        "sanitation",
        "roads",
        "streetlights",
        "other",
    ]
    assert [p.value for p in Priority] == ["high", "normal", "low"]
    assert [s.value for s in Status] == ["open", "in_progress", "resolved", "rejected"]
    assert [t.value for t in TriagedBy] == ["llm:groq", "llm:ollama", "rules", "rules:fallback", "simulated"]


def test_enums_serialize_as_plain_strings() -> None:
    assert json.dumps({"category": Category.water}) == '{"category": "water"}'
    assert Status("in_progress") is Status.in_progress
