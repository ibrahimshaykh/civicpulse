"""A network-free stand-in for a real LLM provider (task AI-02), selected by
`TRIAGE_PROVIDER=simulated`. CI runs with this provider so the AI-layer
tests never touch the network and never depend on Groq being reachable
(plan §11.11: "no network, ever").
"""

import asyncio
import hashlib
import random
from typing import Literal

import httpx
from openai import RateLimitError

from app.providers.triage.base import TriageResult
from app.providers.triage.parsing import parse_triage_output
from app.providers.triage.rules import RuleBasedTriage

FailureMode = Literal["none", "raise", "timeout", "malformed", "rate_limited"]


class SimulatedProviderError(Exception):
    """Injected failure from SimulatedTriage's "raise" mode."""


class SimulatedTriage:
    name = "simulated"

    def __init__(self, *, seed: int, failure_mode: FailureMode, delay_s: float = 0.0) -> None:
        self._seed = seed
        self._failure_mode = failure_mode
        self._delay_s = delay_s

    async def triage(self, text: str, location: str) -> TriageResult:
        match self._failure_mode:
            case "raise":
                raise SimulatedProviderError("injected failure")
            case "timeout":
                await asyncio.sleep(3600)  # the caller's own timeout cancels this
            case "rate_limited":
                raise _simulated_rate_limit_error()
            case "malformed":
                return parse_triage_output('```json\n{"category": "flooding"}\n```')

        if self._delay_s:
            await asyncio.sleep(self._delay_s)

        base = RuleBasedTriage().triage_sync(text, location)
        rng = random.Random(f"{self._seed}:{hashlib.sha256(text.encode()).hexdigest()}")  # noqa: S311 -- deterministic, not cryptographic
        return base.model_copy(
            update={
                "confidence": round(0.6 + 0.4 * rng.random(), 2),
                "summary": f"[sim] {base.summary}"[:140],
            }
        )


def _simulated_rate_limit_error() -> RateLimitError:
    """Build a real `openai.RateLimitError` so the retry policy (AI-05) sees
    exactly what it would see from the genuine SDK, without a live server.
    """
    request = httpx.Request("POST", "https://simulated.invalid/v1/chat/completions")
    response = httpx.Response(429, request=request, json={"error": {"message": "simulated rate limit"}})
    return RateLimitError("simulated rate limit", response=response, body=None)
