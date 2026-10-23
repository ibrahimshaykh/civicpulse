"""AI-02 acceptance (plan §11.13, test A18 + failure-mode coverage)."""

import asyncio

import pytest
from openai import RateLimitError

from app.providers.triage.base import TriageResult
from app.providers.triage.parsing import MalformedOutput
from app.providers.triage.simulated import SimulatedProviderError, SimulatedTriage

COMPLAINTS = [
    "Burst water main flooding homes since dawn",
    "Live wire hanging from a pole after the storm",
    "Kachra not collected for 10 days near the park",
    "Traffic signal not working at the main chowk",
]


async def test_A18_same_seed_and_text_is_identical_across_100_calls() -> None:
    provider = SimulatedTriage(seed=42, failure_mode="none")
    for text in COMPLAINTS:
        outputs = {await provider.triage(text, "somewhere") for _ in range(25)}
        assert len(outputs) == 1


async def test_different_seeds_can_disagree_on_confidence() -> None:
    a = await SimulatedTriage(seed=1, failure_mode="none").triage(COMPLAINTS[0], "x")
    b = await SimulatedTriage(seed=2, failure_mode="none").triage(COMPLAINTS[0], "x")
    assert a.category == b.category  # same underlying rules classification
    assert a.confidence != b.confidence  # but a seed-dependent confidence


async def test_raise_mode_raises_simulated_provider_error() -> None:
    with pytest.raises(SimulatedProviderError):
        await SimulatedTriage(seed=1, failure_mode="raise").triage("x", "y")


async def test_malformed_mode_raises_malformed_output() -> None:
    with pytest.raises(MalformedOutput):
        await SimulatedTriage(seed=1, failure_mode="malformed").triage("x", "y")


async def test_rate_limited_mode_raises_openai_rate_limit_error() -> None:
    with pytest.raises(RateLimitError):
        await SimulatedTriage(seed=1, failure_mode="rate_limited").triage("x", "y")


async def test_timeout_mode_is_cancellable_by_the_caller() -> None:
    """The mode sleeps for an hour; a real caller wraps it in asyncio.timeout
    (AI-05). Here we prove it is a plain cancellable sleep, not a busy loop."""
    task = asyncio.ensure_future(SimulatedTriage(seed=1, failure_mode="timeout").triage("x", "y"))
    await asyncio.sleep(0)  # let it start sleeping
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task


async def test_no_network_socket_opened_for_a_normal_call(monkeypatch: pytest.MonkeyPatch) -> None:
    """Guards plan §11.11's "no network, ever": block socket creation and
    confirm a normal call still succeeds."""
    import socket

    def _blocked(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("SimulatedTriage must never open a socket")

    monkeypatch.setattr(socket, "socket", _blocked)
    result = await SimulatedTriage(seed=1, failure_mode="none").triage(COMPLAINTS[0], "x")
    assert isinstance(result, TriageResult)
