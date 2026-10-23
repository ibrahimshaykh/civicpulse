"""Shared by every LLM-backed provider (Groq, Ollama, and SimulatedTriage's
"malformed" failure mode): turns raw model output into a `TriageResult`,
strictly. No fence stripping, no eval, no regex extraction -- a model that
does not return exactly the documented JSON shape is a `MalformedOutput`,
which the caller (`TriageService`) always treats as a fallback, never as
"best effort" (plan §11.3 guardrail layer 4).
"""

from pydantic import ValidationError

from app.providers.triage.base import TriageResult


class MalformedOutput(Exception):
    """Model returned something that is not a valid TriageResult. Never retried."""


def parse_triage_output(raw: str) -> TriageResult:
    if len(raw) > 2_000:
        raise MalformedOutput("output too long")
    try:
        return TriageResult.model_validate_json(raw)
    except ValidationError as e:
        # include_input=False: the raw model output could echo PII: never logged.
        raise MalformedOutput(e.errors(include_url=False, include_input=False)) from None
