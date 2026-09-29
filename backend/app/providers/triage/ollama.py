"""OllamaTriage (task AI-09): the `ollama` primary provider, calling a
local Ollama server's chat API with a JSON-schema-constrained response.

No PII redaction here (unlike GroqTriage): nothing leaves the machine
running Ollama, so there is no third party to withhold PII from. Still
harmless to redact, but the plan is explicit that it's unnecessary.

`self._http` is a shared `httpx.AsyncClient` owned by the app's lifespan
(`core/lifecycle.py`), not by this instance -- unlike GroqTriage's own
`AsyncOpenAI` client, there is no `aclose()` here.
"""

import httpx

from app.providers.triage.base import TriageResult
from app.providers.triage.errors import OllamaServerError
from app.providers.triage.parsing import parse_triage_output
from app.providers.triage.prompt import build_messages


class OllamaTriage:
    name = "llm:ollama"

    def __init__(self, *, http: httpx.AsyncClient, base_url: str, model: str, timeout_s: float) -> None:
        self._http = http
        self._base = base_url
        self.model = model
        self._timeout_s = timeout_s

    async def triage(self, text: str, location: str) -> TriageResult:
        r = await self._http.post(
            f"{self._base}/api/chat",
            timeout=self._timeout_s,
            json={
                "model": self.model,
                "messages": build_messages(text),
                "stream": False,
                "format": TriageResult.model_json_schema(),
                "options": {"temperature": 0, "num_predict": 200},
            },
        )
        if r.status_code >= 500:
            raise OllamaServerError(r.status_code)
        r.raise_for_status()
        return parse_triage_output(r.json()["message"]["content"])
