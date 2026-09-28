"""AI-10/AI-11 acceptance: /api/meta/providers reports the real active
provider and model, and is honest that no cache hit rate exists yet
(AI-08 hasn't landed)."""

from app.core.config import Settings


class FakeTriageService:
    def __init__(self, active_provider: str, outcomes: list[dict[str, object]]) -> None:
        self.active_provider = active_provider
        self._outcomes = outcomes

    async def recent_outcomes(self) -> list[dict[str, object]]:
        return self._outcomes


def _settings() -> Settings:
    return Settings(postgres_password="x", redis_password="x")  # type: ignore[call-arg]


async def test_reports_the_model_for_a_known_provider() -> None:
    from app.services.meta_service import MetaService

    svc = MetaService(FakeTriageService("llm:groq", []), _settings())  # type: ignore[arg-type]
    out = await svc.providers()
    assert out.active_provider == "llm:groq"
    assert out.model == "llama-3.1-8b-instant"
    assert out.fallback_provider == "rules"


async def test_model_is_none_for_rules_or_simulated() -> None:
    from app.services.meta_service import MetaService

    svc = MetaService(FakeTriageService("rules", []), _settings())  # type: ignore[arg-type]
    out = await svc.providers()
    assert out.model is None


async def test_cache_hit_rate_is_honestly_none_before_ai_08() -> None:
    from app.services.meta_service import MetaService

    svc = MetaService(FakeTriageService("rules", []), _settings())  # type: ignore[arg-type]
    out = await svc.providers()
    assert out.cache_hit_rate is None
