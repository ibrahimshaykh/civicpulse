"""AI-11 acceptance (test A17): each TRIAGE_PROVIDER value selects the right
class, and `llm`/`ollama` (not yet implemented) degrade to rules with an
ERROR log rather than crashing the service."""

import structlog

from app.core.config import Settings
from app.providers.triage.factory import build_primary
from app.providers.triage.rules import RuleBasedTriage
from app.providers.triage.simulated import SimulatedTriage


def _settings(**overrides: object) -> Settings:
    return Settings(postgres_password="x", redis_password="x", **overrides)  # type: ignore[call-arg]


def test_rules_selects_rule_based_triage() -> None:
    assert isinstance(build_primary(_settings(triage_provider="rules")), RuleBasedTriage)


def test_simulated_selects_simulated_triage_with_settings_seed_and_mode() -> None:
    s = _settings(triage_provider="simulated", simulated_seed=7, simulated_failure_mode="raise")
    primary = build_primary(s)
    assert isinstance(primary, SimulatedTriage)
    assert primary._seed == 7  # verifying the factory actually threaded settings through
    assert primary._failure_mode == "raise"


def test_llm_without_groq_implemented_falls_back_to_rules_with_error_log() -> None:
    with structlog.testing.capture_logs() as logs:
        primary = build_primary(_settings(triage_provider="llm"))
    assert isinstance(primary, RuleBasedTriage)
    assert any(entry.get("event") == "triage_provider_not_yet_implemented" for entry in logs)


def test_ollama_without_ollama_implemented_falls_back_to_rules() -> None:
    assert isinstance(build_primary(_settings(triage_provider="ollama")), RuleBasedTriage)
