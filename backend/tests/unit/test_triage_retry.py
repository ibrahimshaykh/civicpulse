"""AI-05 acceptance (plan §11.13, tests A3-A7): exactly one retry, only for
retryable errors, with injectable sleep/rng so timing is deterministic."""

import asyncio
import random
from uuid import uuid4

import httpx
from openai import BadRequestError, RateLimitError

from app.domain.enums import Category, Priority
from app.providers.triage.base import TriageResult
from app.providers.triage.parsing import MalformedOutput
from app.services.triage_service import TriageService

RESULT = TriageResult(category=Category.other, priority=Priority.normal, summary="x", confidence=0.5)


class CountingProvider:
    name = "llm:groq"

    def __init__(self, exc: Exception) -> None:
        self._exc = exc
        self.calls = 0

    async def triage(self, text: str, location: str) -> TriageResult:
        self.calls += 1
        raise self._exc


class SlowProvider:
    name = "llm:groq"

    def __init__(self, sleep_s: float) -> None:
        self._sleep_s = sleep_s

    async def triage(self, text: str, location: str) -> TriageResult:
        await asyncio.sleep(self._sleep_s)
        return RESULT


class FlakyOnceProvider:
    """Fails once with a retryable error, then succeeds."""

    name = "llm:groq"

    def __init__(self, exc: Exception) -> None:
        self._exc = exc
        self.calls = 0

    async def triage(self, text: str, location: str) -> TriageResult:
        self.calls += 1
        if self.calls == 1:
            raise self._exc
        return RESULT


def _fake_rate_limit_error() -> RateLimitError:
    request = httpx.Request("POST", "https://api.groq.com/openai/v1/chat/completions")
    response = httpx.Response(429, request=request, json={"error": {"message": "rate limited"}})
    return RateLimitError("rate limited", response=response, body=None)


def _fake_bad_request_error() -> BadRequestError:
    request = httpx.Request("POST", "https://api.groq.com/openai/v1/chat/completions")
    response = httpx.Response(400, request=request, json={"error": {"message": "bad request"}})
    return BadRequestError("bad request", response=response, body=None)


async def _no_sleep(_seconds: float) -> None:
    return None


async def test_A3_rate_limit_retries_exactly_once_then_falls_back() -> None:
    provider = CountingProvider(_fake_rate_limit_error())
    svc = TriageService(provider, sleep=_no_sleep, rng=random.Random(0))

    outcome = await svc.triage(complaint_id=uuid4(), text="x", location="y")

    assert provider.calls == 2
    assert outcome.fallback is True
    assert outcome.error_class == "RateLimitError"


async def test_A4_bad_request_is_never_retried() -> None:
    provider = CountingProvider(_fake_bad_request_error())
    svc = TriageService(provider, sleep=_no_sleep, rng=random.Random(0))

    outcome = await svc.triage(complaint_id=uuid4(), text="x", location="y")

    assert provider.calls == 1
    assert outcome.fallback is True
    assert outcome.error_class == "BadRequestError"


async def test_A5_malformed_output_is_never_retried() -> None:
    provider = CountingProvider(MalformedOutput("bad shape"))
    svc = TriageService(provider, sleep=_no_sleep, rng=random.Random(0))

    outcome = await svc.triage(complaint_id=uuid4(), text="x", location="y")

    assert provider.calls == 1
    assert outcome.fallback is True
    assert outcome.error_class == "MalformedOutput"


async def test_A6_hard_timeout_falls_back_fast() -> None:
    provider = SlowProvider(sleep_s=60)
    svc = TriageService(provider, timeout_s=0.05, sleep=_no_sleep, rng=random.Random(0))

    start = asyncio.get_event_loop().time()
    outcome = await svc.triage(complaint_id=uuid4(), text="x", location="y")
    elapsed = asyncio.get_event_loop().time() - start

    assert outcome.fallback is True
    assert outcome.error_class == "TimeoutError"
    assert elapsed < 1.0


async def test_A7_jitter_delay_is_within_the_configured_bounds() -> None:
    provider = CountingProvider(_fake_rate_limit_error())
    recorded: list[float] = []

    async def recording_sleep(seconds: float) -> None:
        recorded.append(seconds)

    svc = TriageService(provider, sleep=recording_sleep, rng=random.Random(0), jitter_s=(0.2, 0.8))
    await svc.triage(complaint_id=uuid4(), text="x", location="y")

    assert len(recorded) == 1
    assert 0.2 <= recorded[0] <= 0.8


async def test_a_successful_retry_returns_the_second_attempts_result() -> None:
    """Not in A3-A7, but the natural complement: a retryable failure followed
    by success should NOT fall back at all."""
    provider = FlakyOnceProvider(_fake_rate_limit_error())
    svc = TriageService(provider, sleep=_no_sleep, rng=random.Random(0))

    outcome = await svc.triage(complaint_id=uuid4(), text="x", location="y")

    assert provider.calls == 2
    assert outcome.fallback is False
    assert outcome.triaged_by == "llm:groq"
    assert outcome.result == RESULT
