"""AI-10/AI-11/AI-08 acceptance: /api/meta/providers reports the real
active provider and model, and reports the cache's real hit rate (honestly
None when nothing has been cached yet)."""

from app.core.config import Settings


class FakeTriageService:
    def __init__(
        self, active_provider: str, outcomes: list[dict[str, object]], hit_rate: float | None = None
    ) -> None:
        self.active_provider = active_provider
        self._outcomes = outcomes
        self._hit_rate = hit_rate

    async def recent_outcomes(self) -> list[dict[str, object]]:
        return self._outcomes

    async def cache_hit_rate(self) -> float | None:
        return self._hit_rate


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


async def test_cache_hit_rate_is_honestly_none_before_anything_is_cached() -> None:
    from app.services.meta_service import MetaService

    svc = MetaService(FakeTriageService("rules", [], hit_rate=None), _settings())  # type: ignore[arg-type]
    out = await svc.providers()
    assert out.cache_hit_rate is None


async def test_cache_hit_rate_is_reported_once_the_cache_has_seen_traffic() -> None:
    from app.services.meta_service import MetaService

    svc = MetaService(FakeTriageService("llm:groq", [], hit_rate=0.36), _settings())  # type: ignore[arg-type]
    out = await svc.providers()
    assert out.cache_hit_rate == 0.36
