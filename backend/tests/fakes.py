"""Fakes shared across test modules -- not a `conftest.py` fixture, because
these are also meant to be imported directly by whoever is coding against
the triage seam ahead of the real implementation (plan §2.2: "Until B's
implementation lands, A uses tests/fakes.py::StubTriageService").
"""

from uuid import UUID

from app.domain.enums import Category, Priority
from app.providers.triage.base import TriageResult
from app.services.triage_service import TriageOutcome


class StubTriageService:
    """A `TriageService` stand-in with the same public surface, returning a
    fixed `TriageOutcome` regardless of input. Lets `ComplaintService` (and
    its tests) be written against the seam without a real provider wired up.
    """

    active_provider = "rules"

    def __init__(self, outcome: TriageOutcome | None = None) -> None:
        self._outcome = outcome or TriageOutcome(
            result=TriageResult(
                category=Category.other, priority=Priority.normal, summary="Stub summary", confidence=0.5
            ),
            triaged_by="rules",
            latency_ms=0,
            cache_hit=False,
            fallback=False,
            error_class=None,
        )
        self.calls: list[tuple[UUID, str, str]] = []

    async def triage(self, *, complaint_id: UUID, text: str, location: str) -> TriageOutcome:
        self.calls.append((complaint_id, text, location))
        return self._outcome

    async def recent_outcomes(self) -> list[dict[str, object]]:
        return []
