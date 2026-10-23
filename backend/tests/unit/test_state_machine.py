"""BE-04 acceptance: all 16 (from, to) pairs parametrized, exactly 4 allowed."""

import pytest

from app.domain.enums import Status
from app.domain.state_machine import allowed_from, is_allowed

ALL_PAIRS = [(f, t) for f in Status for t in Status]
ALLOWED_PAIRS = {
    (Status.open, Status.in_progress),
    (Status.open, Status.rejected),
    (Status.in_progress, Status.resolved),
    (Status.in_progress, Status.rejected),
}


@pytest.mark.parametrize(("current", "target"), ALL_PAIRS)
def test_every_pair_matches_the_expected_table(current: Status, target: Status) -> None:
    assert is_allowed(current, target) == ((current, target) in ALLOWED_PAIRS)


def test_exactly_four_pairs_are_allowed() -> None:
    allowed = [(f, t) for f, t in ALL_PAIRS if is_allowed(f, t)]
    assert len(allowed) == 4


def test_resolved_and_rejected_are_terminal() -> None:
    assert allowed_from(Status.resolved) == []
    assert allowed_from(Status.rejected) == []


def test_allowed_from_is_sorted_by_enum_declaration_order() -> None:
    assert allowed_from(Status.open) == [Status.in_progress, Status.rejected]
