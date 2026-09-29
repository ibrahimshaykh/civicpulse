"""Selects the primary provider from `TRIAGE_PROVIDER` and assembles the
real `TriageService` (task AI-11). The one place that imports every
concrete provider -- `lifecycle.py` calls only `build_triage_service`, so
adding a provider never touches the app's wiring, just this file.
"""

import httpx
import structlog
from redis.asyncio import Redis

from app.core.config import Settings
from app.providers.triage.base import TriageProvider
from app.providers.triage.cache import TriageResultCache
from app.providers.triage.llm import GroqTriage
from app.providers.triage.ollama import OllamaTriage
from app.providers.triage.outcomes import OutcomeLog
from app.providers.triage.rules import RuleBasedTriage
from app.providers.triage.simulated import SimulatedTriage
from app.services.triage_service import TriageService

log = structlog.get_logger()


def build_primary(s: Settings, http: httpx.AsyncClient) -> TriageProvider:
    match s.triage_provider:
        case "llm":
            if s.groq_api_key is None:
                # Never crash the service over a missing key -- degrade to
                # rules, loudly, so a misconfigured deploy still serves traffic.
                log.error("groq_key_missing_falling_back_to_rules")
                return RuleBasedTriage()
            return GroqTriage(
                api_key=s.groq_api_key,
                model=s.groq_model,
                base_url=s.groq_base_url,
                timeout_s=s.triage_timeout_s,
            )
        case "ollama":
            return OllamaTriage(
                http=http, base_url=s.ollama_base_url, model=s.ollama_model, timeout_s=s.triage_timeout_s
            )
        case "rules":
            return RuleBasedTriage()
        case "simulated":
            return SimulatedTriage(seed=s.simulated_seed, failure_mode=s.simulated_failure_mode)
    # Settings' Literal type already rejects any other value at construction time.
    raise AssertionError(f"unreachable: {s.triage_provider}")


def build_triage_service(s: Settings, redis: Redis, http: httpx.AsyncClient) -> TriageService:
    return TriageService(
        build_primary(s, http),
        fallback=RuleBasedTriage(),
        cache=TriageResultCache(redis),
        outcomes=OutcomeLog(redis),
        timeout_s=s.triage_timeout_s,
    )
