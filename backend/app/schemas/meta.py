from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TriageOutcomeOut(BaseModel):
    complaint_id: UUID
    provider: str  # a TriagedBy value
    latency_ms: int
    fallback: bool
    cache_hit: bool
    error_class: str | None
    at: datetime


class ProvidersOut(BaseModel):
    active_provider: str  # e.g. "llm:groq"
    fallback_provider: str  # "rules"
    model: str | None  # e.g. "llama-3.1-8b-instant"
    cache_hit_rate: float | None  # hits / (hits + misses) since process start, Redis-backed
    recent: list[TriageOutcomeOut]  # newest first, max 20
