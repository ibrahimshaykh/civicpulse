"""The triage seam (task C0-04), frozen on Day 2 so Partner A can code
`ComplaintService` against it before any real provider exists.

`TriageResult` is what every provider returns. `TriageProvider` is the
Protocol every provider (rules, simulated, Groq, Ollama) implements.
Nothing outside `app/providers/triage/` and `app/services/triage_service.py`
may import a concrete provider -- callers depend on this module and on
`TriageService`, never on `rules.py` or `simulated.py` directly (plan §2.2,
§10.1's layering rule).
"""

from typing import Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import Category, Priority


class TriageResult(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    category: Category
    priority: Priority
    summary: str = Field(min_length=1, max_length=140)
    confidence: float = Field(ge=0.0, le=1.0)


@runtime_checkable
class TriageProvider(Protocol):
    name: str  # "llm:groq" | "llm:ollama" | "rules" | "simulated"

    async def triage(self, text: str, location: str) -> TriageResult: ...
