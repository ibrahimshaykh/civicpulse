"""Backs `GET /api/meta/providers` (task AI-10). Reads only through
`TriageService`'s public surface (`active_provider`, `recent_outcomes()`),
never a concrete provider or `app.providers.triage.*` directly.
"""

from app.core.config import Settings
from app.schemas import ProvidersOut, TriageOutcomeOut
from app.services.triage_service import TriageService


class MetaService:
    def __init__(self, triage: TriageService, settings: Settings) -> None:
        self._triage = triage
        self._settings = settings

    async def providers(self) -> ProvidersOut:
        active = self._triage.active_provider
        model = {"llm:groq": self._settings.groq_model, "llm:ollama": self._settings.ollama_model}.get(active)
        recent = [TriageOutcomeOut.model_validate(o) for o in await self._triage.recent_outcomes()]
        return ProvidersOut(
            active_provider=active,
            fallback_provider="rules",
            model=model,
            # AI-08's content-hash cache reports the measured hit rate; until
            # then, "we don't have one yet" is more honest than a fake number.
            cache_hit_rate=None,
            recent=recent,
        )
