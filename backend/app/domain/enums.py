"""Domain enums shared by the API, the database and the triage layer.

StrEnum serializes to the plain string, so OpenAPI shows ``enum: ["water", ...]``
and the generated TypeScript type is a string-literal union.
"""

from enum import StrEnum


class Category(StrEnum):
    water = "water"
    electricity = "electricity"
    sanitation = "sanitation"
    roads = "roads"
    streetlights = "streetlights"
    other = "other"


class Priority(StrEnum):
    high = "high"
    normal = "normal"
    low = "low"


class Status(StrEnum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    rejected = "rejected"


class TriagedBy(StrEnum):
    llm_groq = "llm:groq"
    llm_ollama = "llm:ollama"
    rules = "rules"
    rules_fallback = "rules:fallback"
    # Not in the brief's list; added so SimulatedTriage has an honest label (plan §1.3).
    simulated = "simulated"
