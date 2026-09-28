"""AI-03 acceptance (plan §11.13, test A1) and the rest of the skeleton's
fallback contract. Retries (AI-05) are a separate task; the real Redis
`TriageCache`/`OutcomeSink` implementations (AI-08, AI-10) have their own
test files -- here they're exercised only through fakes."""

import asyncio
from uuid import uuid4

import pytest

from app.domain.enums import Category, Priority
from app.providers.triage.base import TriageResult
from app.providers.triage.rules import RuleBasedTriage
from app.services.triage_service import NullOutcomeSink, NullTriageCache, TriageOutcome, TriageService


class AlwaysRaisesProvider:
    name = "llm:groq"

    async def triage(self, text: str, location: str) -> TriageResult:
        raise RuntimeError("primary is down")


class FixedProvider:
    def __init__(self, name: str, result: TriageResult) -> None:
        self.name = name
        self._result = result
        self.calls = 0

    async def triage(self, text: str, location: str) -> TriageResult:
        self.calls += 1
        return self._result


class RecordingOutcomeSink(NullOutcomeSink):
    def __init__(self) -> None:
        self.recorded: list[tuple[object, TriageOutcome]] = []

    async def record(self, complaint_id: object, outcome: TriageOutcome) -> None:
        self.recorded.append((complaint_id, outcome))


class FakeCache(NullTriageCache):
    def __init__(self) -> None:
        self.store: dict[str, TriageResult] = {}

    def key(self, *, provider: str, model: str, text: str) -> str:
        return f"{provider}:{model}:{text}"

    async def get(self, key: str) -> TriageResult | None:
        return self.store.get(key)

    async def set(self, key: str, result: TriageResult) -> None:
        self.store[key] = result


RESULT = TriageResult(category=Category.roads, priority=Priority.normal, summary="A pothole", confidence=0.8)


async def test_A1_always_raises_provider_falls_back_to_rules() -> None:
    svc = TriageService(AlwaysRaisesProvider())
    outcome = await svc.triage(
        complaint_id=uuid4(), text="Bohat bara gaddha on the service road", location="x"
    )
    assert outcome.triaged_by == "rules:fallback"
    assert outcome.fallback is True
    assert outcome.error_class == "RuntimeError"
    assert isinstance(outcome.result, TriageResult)


async def test_successful_primary_is_not_marked_as_fallback() -> None:
    provider = FixedProvider("llm:groq", RESULT)
    svc = TriageService(provider)
    outcome = await svc.triage(complaint_id=uuid4(), text="A pothole on the road", location="x")
    assert outcome.fallback is False
    assert outcome.triaged_by == "llm:groq"
    assert outcome.error_class is None
    assert outcome.result == RESULT


async def test_active_provider_reports_the_primarys_name() -> None:
    svc = TriageService(FixedProvider("llm:ollama", RESULT))
    assert svc.active_provider == "llm:ollama"


async def test_recent_outcomes_delegates_to_the_outcome_sink() -> None:
    sink = RecordingOutcomeSink()
    svc = TriageService(FixedProvider("llm:groq", RESULT), outcomes=sink)
    complaint_id = uuid4()
    await svc.triage(complaint_id=complaint_id, text="A pothole on the road", location="x")
    assert len(sink.recorded) == 1
    assert sink.recorded[0][0] == complaint_id
    assert await svc.recent_outcomes() == []  # NullOutcomeSink.recent() default; AI-10 replaces it


async def test_cache_hit_rate_is_none_before_ai_08s_cache_is_configured() -> None:
    svc = TriageService(FixedProvider("llm:groq", RESULT))  # default NullTriageCache
    assert await svc.cache_hit_rate() is None


async def test_cache_hit_rate_delegates_to_the_cache() -> None:
    class HitRateCache(NullTriageCache):
        async def hit_rate(self) -> float | None:
            return 0.36

    svc = TriageService(FixedProvider("llm:groq", RESULT), cache=HitRateCache())
    assert await svc.cache_hit_rate() == 0.36


async def test_cache_hit_skips_the_primary_and_is_flagged() -> None:
    cache = FakeCache()
    provider = FixedProvider("llm:groq", RESULT)
    svc = TriageService(provider, cache=cache)
    complaint_id = uuid4()

    first = await svc.triage(complaint_id=complaint_id, text="A pothole on the road", location="x")
    second = await svc.triage(complaint_id=complaint_id, text="A pothole on the road", location="x")

    assert provider.calls == 1  # the primary is only ever called once
    assert first.cache_hit is False
    assert second.cache_hit is True
    assert second.result == RESULT


async def test_rules_as_primary_never_touches_the_cache() -> None:
    """When rules *is* the primary, there is nothing to cache: rules are
    cheaper than a Redis round-trip (plan §11.6)."""
    cache = FakeCache()
    svc = TriageService(RuleBasedTriage(), cache=cache)
    await svc.triage(complaint_id=uuid4(), text="A pothole on the road", location="x")
    assert cache.store == {}


async def test_fallback_result_is_not_cached() -> None:
    """A9: a fallback outcome must not poison the cache with a degraded
    result that a later, healthy primary call could have done better."""
    cache = FakeCache()
    svc = TriageService(AlwaysRaisesProvider(), cache=cache)
    await svc.triage(complaint_id=uuid4(), text="A pothole on the road", location="x")
    assert cache.store == {}


async def test_cancelled_error_propagates_instead_of_falling_back() -> None:
    """Shutdown (BE-06) must still be able to cancel an in-flight triage call;
    `except Exception` (not `BaseException`) is what makes this possible."""

    class CancellingProvider:
        name = "llm:groq"

        async def triage(self, text: str, location: str) -> TriageResult:
            raise asyncio.CancelledError

    svc = TriageService(CancellingProvider())
    with pytest.raises(asyncio.CancelledError):
        await svc.triage(complaint_id=uuid4(), text="x", location="y")
