"""GroqTriage (task AI-04): the `llm` primary provider, calling an
OpenAI-compatible chat-completions endpoint (Groq) in JSON mode.

`max_retries=0` on the SDK client is load-bearing, not a stray default:
TriageService (AI-05) owns the one retry, with its own jittered sleep. If
the SDK also retried, a single primary call could silently become up to
3 attempts and blow past the documented 21s worst-case budget.
"""

from typing import cast

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam
from pydantic import SecretStr

from app.providers.triage.base import TriageResult
from app.providers.triage.parsing import parse_triage_output
from app.providers.triage.prompt import build_messages
from app.providers.triage.redaction import redact


class GroqTriage:
    name = "llm:groq"

    def __init__(self, *, api_key: SecretStr, model: str, base_url: str, timeout_s: float) -> None:
        self.model = model
        self._client = AsyncOpenAI(
            api_key=api_key.get_secret_value(),
            base_url=base_url,
            timeout=timeout_s,
            max_retries=0,
        )

    async def triage(self, text: str, location: str) -> TriageResult:
        # location and reporter_contact are never sent to the LLM (ADR 0004);
        # only the free-text complaint is, and only after PII redaction.
        resp = await self._client.chat.completions.create(
            model=self.model,
            messages=cast(list[ChatCompletionMessageParam], build_messages(redact(text))),
            response_format={"type": "json_object"},
            temperature=0,
            max_tokens=200,
        )
        raw = resp.choices[0].message.content or ""
        return parse_triage_output(raw)

    async def aclose(self) -> None:
        await self._client.close()
