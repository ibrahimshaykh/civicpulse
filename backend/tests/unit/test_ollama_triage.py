"""AI-09 acceptance: OllamaTriage posts to a local Ollama server's chat API
with a JSON-schema-constrained response, maps a 5xx to the retryable
`OllamaServerError` (never falls through to a generic HTTP error for that
case), and applies the same strict parsing as every other LLM provider.
No live Ollama server in this sandbox, so every test mocks the shared
`httpx.AsyncClient` -- the same "no live call in the suite" rule
test_llm_triage.py already follows for Groq.
"""

import json
from unittest.mock import AsyncMock

import httpx
import pytest

from app.providers.triage.base import TriageResult
from app.providers.triage.errors import OllamaServerError
from app.providers.triage.ollama import OllamaTriage
from app.providers.triage.parsing import MalformedOutput

BASE_URL = "http://ollama:11434"
REQUEST = httpx.Request("POST", f"{BASE_URL}/api/chat")

VALID_JSON = json.dumps(
    {"category": "roads", "priority": "normal", "summary": "Pothole on Main St.", "confidence": 0.8}
)


def _response(status_code: int, *, content: str | None = None) -> httpx.Response:
    body = {"message": {"content": content}} if content is not None else {}
    return httpx.Response(status_code, json=body, request=REQUEST)


def _provider(post: AsyncMock, *, timeout_s: float = 10.0) -> OllamaTriage:
    http = AsyncMock(spec=httpx.AsyncClient)
    http.post = post
    return OllamaTriage(http=http, base_url=BASE_URL, model="llama3.2:1b", timeout_s=timeout_s)


def test_name_is_llm_ollama() -> None:
    assert OllamaTriage.name == "llm:ollama"


async def test_valid_response_parses_into_a_triage_result() -> None:
    post = AsyncMock(return_value=_response(200, content=VALID_JSON))
    provider = _provider(post)

    result = await provider.triage("Pothole on Main St", "Main St")

    assert isinstance(result, TriageResult)
    assert result.category == "roads"
    assert result.priority == "normal"


async def test_request_posts_to_api_chat_with_json_schema_format_and_zero_temperature() -> None:
    post = AsyncMock(return_value=_response(200, content=VALID_JSON))
    provider = _provider(post, timeout_s=7.5)

    await provider.triage("text", "loc")

    post.assert_awaited_once()
    (url,), kwargs = post.call_args
    assert url == f"{BASE_URL}/api/chat"
    assert kwargs["timeout"] == 7.5
    body = kwargs["json"]
    assert body["model"] == "llama3.2:1b"
    assert body["stream"] is False
    assert body["format"] == TriageResult.model_json_schema()
    assert body["options"] == {"temperature": 0, "num_predict": 200}


async def test_no_redaction_is_applied_unlike_groq_since_nothing_leaves_the_machine() -> None:
    post = AsyncMock(return_value=_response(200, content=VALID_JSON))
    provider = _provider(post)
    text_with_cnic = "My CNIC is 12345-1234567-1, pothole on Main St"

    await provider.triage(text_with_cnic, "somewhere")

    body = post.call_args.kwargs["json"]
    assert "12345-1234567-1" in json.dumps(body["messages"])


async def test_server_error_raises_ollama_server_error_with_the_status_code() -> None:
    post = AsyncMock(return_value=_response(503))
    provider = _provider(post)

    with pytest.raises(OllamaServerError) as exc_info:
        await provider.triage("text", "loc")
    assert exc_info.value.status_code == 503


async def test_client_error_raises_http_status_error_not_ollama_server_error() -> None:
    post = AsyncMock(return_value=_response(404))
    provider = _provider(post)

    with pytest.raises(httpx.HTTPStatusError):
        await provider.triage("text", "loc")


async def test_malformed_content_raises_malformed_output() -> None:
    post = AsyncMock(return_value=_response(200, content="not json at all"))
    provider = _provider(post)

    with pytest.raises(MalformedOutput):
        await provider.triage("text", "loc")


async def test_invalid_enum_value_raises_malformed_output() -> None:
    bad = json.dumps({"category": "hacked", "priority": "high", "summary": "x", "confidence": 0.5})
    post = AsyncMock(return_value=_response(200, content=bad))
    provider = _provider(post)

    with pytest.raises(MalformedOutput):
        await provider.triage("text", "loc")
