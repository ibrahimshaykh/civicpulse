"""Deterministic keyword-based triage (task AI-01). This is the fallback
every LLM provider degrades to, and it is also selectable directly via
`TRIAGE_PROVIDER=rules` (plan §11.10). It never raises for any string that
passed `ComplaintCreate`'s length validation.
"""

from types import MappingProxyType
from typing import Final

from app.domain.enums import Category, Priority
from app.providers.triage.base import TriageResult
from app.providers.triage.text import first_sentence, normalize

KEYWORDS: Final[dict[Category, tuple[str, ...]]] = {
    Category.water: (
        "water",
        "pani",
        "pipeline",
        "pipe",
        "leak",
        "tanker",
        "supply",
        "valve",
        "tank",
        "burst main",
    ),
    Category.electricity: (
        "electric",
        "bijli",
        "wire",
        "transformer",
        "voltage",
        "load shedding",
        "sparks",
        "pole",
        "meter",
        "current",
    ),
    Category.sanitation: (
        "sewer",
        "sewerage",
        "gutter",
        "garbage",
        "kachra",
        "nullah",
        "drain",
        "dustbin",
        "gandagi",
        "badboo",
        "dead animal",
    ),
    Category.roads: (
        "road",
        "pothole",
        "gaddha",
        "footpath",
        "speed breaker",
        "manhole",
        "signal",
        "dug",
        "carpet",
    ),
    Category.streetlights: ("streetlight", "street light", "light", "lamp", "dark", "andhera", "bulb"),
}
# MappingProxyType so no provider can ever mutate the shared keyword table at runtime.
_KEYWORDS: Final = MappingProxyType(KEYWORDS)

HIGH_RISK: Final = (
    "burst",
    "flood",
    "live wire",
    "sparks",
    "fire",
    "open manhole",
    "manhole cover missing",
    "collapse",
    "diarrhea",
    "contaminat",
    "dengue",
    "electrocut",
    "short circuit",
)
LOW_HINTS: Final = ("small", "minor", "blinking", "broken tile", "paint", "request", "cosmetic")


class RuleBasedTriage:
    name = "rules"

    def triage_sync(self, text: str, location: str) -> TriageResult:
        # location is unused by design: rules classify only on complaint text.
        t = normalize(text)
        scores = {c: sum(t.count(k) for k in kws) for c, kws in _KEYWORDS.items()}
        best = max(scores, key=lambda c: (scores[c], -list(Category).index(c)))
        category = best if scores[best] > 0 else Category.other
        priority = (
            Priority.high
            if any(k in t for k in HIGH_RISK)
            else Priority.low
            if any(k in t for k in LOW_HINTS)
            else Priority.normal
        )
        summary = first_sentence(text, limit=120)
        confidence = min(0.9, 0.3 + 0.15 * scores[best]) if scores[best] else 0.2
        return TriageResult(
            category=category, priority=priority, summary=summary, confidence=round(confidence, 2)
        )

    async def triage(self, text: str, location: str) -> TriageResult:
        return self.triage_sync(text, location)
