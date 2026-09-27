"""AI-07 acceptance (plan §11.12, test A14): each PII pattern is redacted;
ordinary numbers that merely look similar are left alone."""

import pytest

from app.providers.triage.redaction import redact


@pytest.mark.parametrize(
    ("text", "expected_marker"),
    [
        ("Call me on 03001234567 please", "[PHONE]"),
        ("Contact +923001234567 for details", "[PHONE]"),
        ("Alt number 00923001234567 works too", "[PHONE]"),
        ("My CNIC is 12345-1234567-1", "[CNIC]"),
        ("CNIC without dashes 1234512345671", "[CNIC]"),
        ("Email me at citizen@example.com", "[EMAIL]"),
        ("House 45, F-11/3, Islamabad", "[ADDRESS]"),
        ("H.No. 210, G-8/1", "[ADDRESS]"),
        ("Plot 12 near the market", "[ADDRESS]"),
    ],
)
def test_A14_each_pii_pattern_is_redacted(text: str, expected_marker: str) -> None:
    assert expected_marker in redact(text)


@pytest.mark.parametrize(
    "text",
    [
        "No water supply for 3 days now",
        "Street 12, G-9/2, Islamabad",
        "Pothole caused 2 bikers to fall",
        "Sewerage line overflow since morning",
    ],
)
def test_ordinary_numbers_and_addresses_are_preserved(text: str) -> None:
    assert redact(text) == text


def test_multiple_patterns_in_the_same_text_are_all_redacted() -> None:
    text = "Call 03001234567 or email citizen@example.com about House 45"
    result = redact(text)
    assert "[PHONE]" in result
    assert "[EMAIL]" in result
    assert "[ADDRESS]" in result
    assert "03001234567" not in result
    assert "citizen@example.com" not in result
