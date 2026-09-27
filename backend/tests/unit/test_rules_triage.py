"""AI-01 acceptance (plan §11.13, test A20 + rule quality checks)."""

import pytest

from app.domain.enums import Category, Priority
from app.providers.triage.base import TriageResult
from app.providers.triage.rules import RuleBasedTriage
from app.seed import load_seed_rows

ACCURACY_THRESHOLD = 0.70


def test_A20_rules_accuracy_on_seed_rows_at_least_70_percent() -> None:
    rows = load_seed_rows()
    rt = RuleBasedTriage()
    correct = sum(rt.triage_sync(r.text, r.location).category == r.category for r in rows)
    accuracy = correct / len(rows)
    assert accuracy >= ACCURACY_THRESHOLD, f"rules accuracy {accuracy:.1%} on {len(rows)} seed rows"


def test_deterministic_for_the_same_input() -> None:
    rt = RuleBasedTriage()
    a = rt.triage_sync("Burst water main flooding homes", "Street 1")
    b = rt.triage_sync("Burst water main flooding homes", "Street 1")
    assert a == b


def test_high_risk_keyword_forces_high_priority() -> None:
    rt = RuleBasedTriage()
    result = rt.triage_sync("Live wire hanging from a pole after the storm", "Street 3")
    assert result.priority == Priority.high


def test_low_hint_keyword_gives_low_priority_absent_a_high_risk_keyword() -> None:
    rt = RuleBasedTriage()
    result = rt.triage_sync("Minor cosmetic paint request for the community board", "Street 3")
    assert result.priority == Priority.low


def test_no_keyword_match_falls_back_to_other() -> None:
    rt = RuleBasedTriage()
    result = rt.triage_sync("The neighbours play loud music every night until 3am", "Street 3")
    assert result.category == Category.other


@pytest.mark.parametrize(
    "text",
    [
        "a" * 10,
        "a" * 2000,
        "!@#$%^&*()_+ punctuation only, no keywords whatsoever!!" * 5,
        "بجلی کا کھمبا گر گیا ہے سڑک پر، بہت خطرناک ہے" * 3,  # non-Latin script
        "WATER water WaTeR ELECTRICITY electricity" * 20,  # every keyword, mixed case, repeated
        "À" * 200,  # combining characters, exercises NFKC normalization
    ],
)
def test_total_for_edge_case_strings_in_the_valid_length_range(text: str) -> None:
    """RuleBasedTriage never raises for any string that passed ComplaintCreate's
    own length validation (plan §11.10: "deterministic, pure, and total")."""
    result = RuleBasedTriage().triage_sync(text, "somewhere")
    assert isinstance(result, TriageResult)
