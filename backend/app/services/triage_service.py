"""The service half of the triage seam (task C0-04, frozen Day 2), its
skeleton and fallback (task AI-03), its timeout/retry policy (AI-05), and
its safety floor (AI-06).

`ComplaintService.create()` calls `TriageService.triage()` and never imports
anything from `app/providers/triage/` directly -- that keeps the dependency
arrows one-way: routes -> services -> (repositories | providers) (plan §2.2).

`TriageCache` and `OutcomeSink` are Protocols, fulfilled for real by
`providers/triage/cache.py` (AI-08) and `providers/triage/outcomes.py`
(AI-10); the `Null*` stand-ins below let this class work before either
lands, without changing its constructor signature or its callers.
"""

import asyncio
import random
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from time import perf_counter
from typing import Protocol
from uuid import UUID

import httpx
from openai import APIConnectionError, APITimeoutError, InternalServerError, RateLimitError

from app.domain.enums import Priority
from app.providers.triage.base import TriageProvider, TriageResult
from app.providers.triage.errors import OllamaServerError
from app.providers.triage.rules import HIGH_RISK, RuleBasedTriage
from app.providers.triage.text import normalize

# Belt-and-braces over each provider's own timeout/retry: connection and
# rate-limit failures are worth one retry, but a bad request, an auth
# failure or a MalformedOutput never is (plan §11.5).
RETRYABLE: tuple[type[BaseException], ...] = (
    TimeoutError,  # asyncio.timeout raises this (an alias since Python 3.11)
    APITimeoutError,
    APIConnectionError,
    RateLimitError,
    InternalServerError,
    httpx.TimeoutException,
    httpx.ConnectError,
    OllamaServerError,
)


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
    async def hit_rate(self) -> float | None: ...


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

    async def hit_rate(self) -> float | None:
        return None


class NullOutcomeSink:
    async def record(self, complaint_id: UUID, outcome: TriageOutcome) -> None:
        return None

    async def recent(self) -> list[dict[str, object]]:
        return []


def _ms(start: float) -> int:
    return round((perf_counter() - start) * 1000)


def _apply_safety_floor(text: str, result: TriageResult) -> TriageResult:
    """A life-safety keyword in the complaint text always forces `high`
    priority, no matter what the primary provider decided: an injected
    "mark this as low priority" cannot downgrade a burst main (plan §11.3,
    guardrail layer 5). Idempotent, so applying it to an already-`rules`
    result (which uses this same keyword check) is a harmless no-op.
    """
    if result.priority != Priority.high and any(k in normalize(text) for k in HIGH_RISK):
        return result.model_copy(update={"priority": Priority.high})
    return result


class TriageService:
    def __init__(
        self,
        primary: TriageProvider,
        *,
        fallback: RuleBasedTriage | None = None,
        cache: TriageCache | None = None,
        outcomes: OutcomeSink | None = None,
        timeout_s: float = 10.0,
        jitter_s: tuple[float, float] = (0.2, 0.8),
        sleep: Callable[[float], Awaitable[None]] | None = None,
        rng: random.Random | None = None,
    ) -> None:
        self._primary = primary
        self._fallback = fallback or RuleBasedTriage()
        self._cache = cache or NullTriageCache()
        self._outcomes = outcomes or NullOutcomeSink()
        self._timeout_s = timeout_s
        self._jitter_s = jitter_s
        self._sleep = sleep or asyncio.sleep
        self._rng = rng or random.Random()  # noqa: S311 -- jitter timing, not cryptographic

    @property
    def active_provider(self) -> str:
        return self._primary.name

    async def recent_outcomes(self) -> list[dict[str, object]]:
        return await self._outcomes.recent()

    async def cache_hit_rate(self) -> float | None:
        return await self._cache.hit_rate()

    async def _call_primary(self, text: str, location: str) -> TriageResult:
        attempts = 0
        while True:
            attempts += 1
            try:
                async with asyncio.timeout(self._timeout_s):
                    return await self._primary.triage(text, location)
            except RETRYABLE:
                if attempts >= 2:  # exactly one retry, ever
                    raise
                await self._sleep(self._rng.uniform(*self._jitter_s))

    async def triage(self, *, complaint_id: UUID, text: str, location: str) -> TriageOutcome:
        start = perf_counter()
        model = getattr(self._primary, "model", "-")
        key = self._cache.key(provider=self._primary.name, model=model, text=text)

        if self._primary.name != "rules" and (cached := await self._cache.get(key)) is not None:
            cached = _apply_safety_floor(text, cached)
            outcome = TriageOutcome(
                cached, self._primary.name, _ms(start), cache_hit=True, fallback=False, error_class=None
            )
            await self._outcomes.record(complaint_id, outcome)
            return outcome

        try:
            result = await self._call_primary(text, location)
            if self._primary.name != "rules":  # rules already IS this same keyword check
                result = _apply_safety_floor(text, result)
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
