"""AI-11 acceptance (test A17): each TRIAGE_PROVIDER value selects the right
class, and `llm` without a configured key degrades to rules with an ERROR
log rather than crashing the service."""

from collections.abc import AsyncIterator

import httpx
import pytest
import structlog

from app.core.config import Settings
from app.providers.triage.factory import build_primary
from app.providers.triage.llm import GroqTriage
from app.providers.triage.ollama import OllamaTriage
from app.providers.triage.rules import RuleBasedTriage
from app.providers.triage.simulated import SimulatedTriage


def _settings(**overrides: object) -> Settings:
    return Settings(postgres_password="x", redis_password="x", **overrides)  # type: ignore[call-arg]


@pytest.fixture
async def http() -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient() as client:
        yield client


async def test_rules_selects_rule_based_triage(http: httpx.AsyncClient) -> None:
    assert isinstance(build_primary(_settings(triage_provider="rules"), http), RuleBasedTriage)


async def test_simulated_selects_simulated_triage_with_settings_seed_and_mode(
    http: httpx.AsyncClient,
) -> None:
    s = _settings(triage_provider="simulated", simulated_seed=7, simulated_failure_mode="raise")
    primary = build_primary(s, http)
    assert isinstance(primary, SimulatedTriage)
    assert primary._seed == 7  # verifying the factory actually threaded settings through
    assert primary._failure_mode == "raise"


async def test_llm_without_groq_key_falls_back_to_rules_with_error_log(http: httpx.AsyncClient) -> None:
    with structlog.testing.capture_logs() as logs:
        primary = build_primary(_settings(triage_provider="llm"), http)
    assert isinstance(primary, RuleBasedTriage)
    assert any(entry.get("event") == "groq_key_missing_falling_back_to_rules" for entry in logs)


async def test_llm_with_groq_key_selects_groq_triage_with_settings_threaded_through(
    http: httpx.AsyncClient,
) -> None:
    s = _settings(
        triage_provider="llm",
        groq_api_key="gsk-test-key",
        groq_model="llama-3.1-8b-instant",
        groq_base_url="https://api.groq.com/openai/v1",
        triage_timeout_s=5.0,
    )
    primary = build_primary(s, http)
    assert isinstance(primary, GroqTriage)
    assert primary.name == "llm:groq"
    assert primary.model == "llama-3.1-8b-instant"


async def test_ollama_selects_ollama_triage_with_settings_threaded_through(http: httpx.AsyncClient) -> None:
    s = _settings(
        triage_provider="ollama",
        ollama_base_url="http://ollama:11434",
        ollama_model="llama3.2:1b",
        triage_timeout_s=5.0,
    )
    primary = build_primary(s, http)
    assert isinstance(primary, OllamaTriage)
    assert primary.name == "llm:ollama"
    assert primary.model == "llama3.2:1b"
