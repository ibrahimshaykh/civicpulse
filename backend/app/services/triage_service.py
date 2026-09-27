"""The service half of the triage seam (task C0-04, frozen Day 2) and its
first real implementation (task AI-03: skeleton + fallback).

`ComplaintService.create()` calls `TriageService.triage()` and never imports
anything from `app/providers/triage/` directly -- that keeps the dependency
arrows one-way: routes -> services -> (repositories | providers) (plan §2.2).

This skeleton does not yet retry (`AI-05`), cache (`AI-08`) or persist
outcomes anywhere durable (`AI-10`): a primary failure of any kind falls
back to `RuleBasedTriage` right away. `TriageCache` and `OutcomeSink` are
Protocols so those later tasks can plug in a Redis-backed implementation
without changing this class's constructor signature or its callers.
"""

from dataclasses import dataclass
from time import perf_counter
from typing import Protocol
from uuid import UUID

from app.providers.triage.base import TriageProvider, TriageResult
from app.providers.triage.rules import RuleBasedTriage


@dataclass(frozen=True, slots=True)
class TriageOutcome:
    result: TriageResult
    triaged_by: str  # "llm:groq" | "llm:ollama" | "rules" | "rules:fallback" | "simulated"
    latency_ms: int
    cache_hit: bool
    fallback: bool
    error_class: str | None  # e.g. "TimeoutError" when fallback is True


class TriageCache(Protocol):
    """Fulfilled for real by `providers/triage/cache.py`'s Redis-backed
    `TriageResultCache` (task AI-08); `NullTriageCache` below is a
    permanent-miss stand-in so `TriageService` works before AI-08 lands.
    """

    def key(self, *, provider: str, model: str, text: str) -> str: ...
    async def get(self, key: str) -> TriageResult | None: ...
    async def set(self, key: str, result: TriageResult) -> None: ...


class OutcomeSink(Protocol):
    """Fulfilled for real by `providers/triage/outcomes.py`'s Redis-backed
    `OutcomeLog` (task AI-10); `NullOutcomeSink` below discards outcomes so
    `TriageService` works before AI-10 lands.
    """

    async def record(self, complaint_id: UUID, outcome: TriageOutcome) -> None: ...
    async def recent(self) -> list[dict[str, object]]: ...


class NullTriageCache:
    def key(self, *, provider: str, model: str, text: str) -> str:
        return ""

    async def get(self, key: str) -> TriageResult | None:
        return None

    async def set(self, key: str, result: TriageResult) -> None:
        return None


class NullOutcomeSink:
    async def record(self, complaint_id: UUID, outcome: TriageOutcome) -> None:
        return None

    async def recent(self) -> list[dict[str, object]]:
        return []


def _ms(start: float) -> int:
    return round((perf_counter() - start) * 1000)


class TriageService:
    def __init__(
        self,
        primary: TriageProvider,
        *,
        fallback: RuleBasedTriage | None = None,
        cache: TriageCache | None = None,
        outcomes: OutcomeSink | None = None,
    ) -> None:
        self._primary = primary
        self._fallback = fallback or RuleBasedTriage()
        self._cache = cache or NullTriageCache()
        self._outcomes = outcomes or NullOutcomeSink()

    @property
    def active_provider(self) -> str:
        return self._primary.name

    async def recent_outcomes(self) -> list[dict[str, object]]:
        return await self._outcomes.recent()

    async def triage(self, *, complaint_id: UUID, text: str, location: str) -> TriageOutcome:
        start = perf_counter()
        model = getattr(self._primary, "model", "-")
        key = self._cache.key(provider=self._primary.name, model=model, text=text)

        if self._primary.name != "rules" and (cached := await self._cache.get(key)) is not None:
            outcome = TriageOutcome(
                cached, self._primary.name, _ms(start), cache_hit=True, fallback=False, error_class=None
            )
            await self._outcomes.record(complaint_id, outcome)
            return outcome

        try:
            result = await self._primary.triage(text, location)
            outcome = TriageOutcome(
                result, self._primary.name, _ms(start), cache_hit=False, fallback=False, error_class=None
            )
            if self._primary.name != "rules":  # success only, and never for rules -- see the read guard above
                await self._cache.set(key, result)
        except Exception as exc:  # deliberate: nothing but CancelledError should ever reach here
            result = self._fallback.triage_sync(text, location)
            outcome = TriageOutcome(
                result,
                "rules:fallback",
                _ms(start),
                cache_hit=False,
                fallback=True,
                error_class=type(exc).__name__,
            )

        await self._outcomes.record(complaint_id, outcome)
        return outcome
