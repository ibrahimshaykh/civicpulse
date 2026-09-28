"""AI-04 acceptance (test A2: manual call succeeds; test A15: no
reporter_contact/location sent, PII redacted). GroqTriage talks to the
network only through the openai SDK client, so every test here patches
`AsyncOpenAI` itself rather than making a real call -- the same "no live
call in the suite" rule AI-02's SimulatedTriage tests already follow.
"""

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import SecretStr

from app.providers.triage import llm as llm_module
from app.providers.triage.base import TriageResult
from app.providers.triage.llm import GroqTriage
from app.providers.triage.parsing import MalformedOutput


def _fake_client(content: str) -> MagicMock:
    completion = SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=content))])
    client = MagicMock()
    client.chat.completions.create = AsyncMock(return_value=completion)
    client.close = AsyncMock()
    return client


def _make_provider(monkeypatch: pytest.MonkeyPatch, content: str) -> tuple[GroqTriage, MagicMock]:
    client = _fake_client(content)
    ctor = MagicMock(return_value=client)
    monkeypatch.setattr(llm_module, "AsyncOpenAI", ctor)
    provider = GroqTriage(
        api_key=SecretStr("gsk-test"),
        model="llama-3.1-8b-instant",
        base_url="https://api.groq.com/openai/v1",
        timeout_s=10.0,
    )
    return provider, ctor


VALID_JSON = json.dumps(
    {"category": "water", "priority": "high", "summary": "Burst main flooding a street.", "confidence": 0.9}
)


async def test_name_is_llm_groq() -> None:
    assert GroqTriage.name == "llm:groq"


async def test_client_disables_sdk_retries_so_triage_service_owns_the_one_retry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, ctor = _make_provider(monkeypatch, VALID_JSON)
    assert ctor.call_args.kwargs["max_retries"] == 0
    assert ctor.call_args.kwargs["api_key"] == "gsk-test"
    assert ctor.call_args.kwargs["base_url"] == "https://api.groq.com/openai/v1"
    assert ctor.call_args.kwargs["timeout"] == 10.0


async def test_a2_valid_response_parses_into_a_triage_result(monkeypatch: pytest.MonkeyPatch) -> None:
    provider, _ = _make_provider(monkeypatch, VALID_JSON)
    result = await provider.triage("Burst main flooding a street", "Main St")
    assert isinstance(result, TriageResult)
    assert result.category == "water"
    assert result.priority == "high"


async def test_request_uses_json_mode_and_zero_temperature(monkeypatch: pytest.MonkeyPatch) -> None:
    provider, ctor = _make_provider(monkeypatch, VALID_JSON)
    await provider.triage("text", "loc")
    kwargs = ctor.return_value.chat.completions.create.call_args.kwargs
    assert kwargs["response_format"] == {"type": "json_object"}
    assert kwargs["temperature"] == 0
    assert kwargs["model"] == "llama-3.1-8b-instant"


async def test_a15_location_and_reporter_contact_are_never_sent(monkeypatch: pytest.MonkeyPatch) -> None:
    provider, ctor = _make_provider(monkeypatch, VALID_JSON)
    location = "42 Secret House, Model Town"
    await provider.triage("plain complaint text", location)
    kwargs = ctor.return_value.chat.completions.create.call_args.kwargs
    sent = json.dumps(kwargs["messages"])
    assert location not in sent


async def test_a15_pii_in_complaint_text_is_redacted_before_sending(monkeypatch: pytest.MonkeyPatch) -> None:
    provider, ctor = _make_provider(monkeypatch, VALID_JSON)
    text_with_cnic = "My CNIC is 12345-1234567-1, water main burst"
    await provider.triage(text_with_cnic, "somewhere")
    kwargs = ctor.return_value.chat.completions.create.call_args.kwargs
    sent = json.dumps(kwargs["messages"])
    assert "12345-1234567-1" not in sent


async def test_malformed_json_raises_malformed_output(monkeypatch: pytest.MonkeyPatch) -> None:
    provider, _ = _make_provider(monkeypatch, "not json at all")
    with pytest.raises(MalformedOutput):
        await provider.triage("text", "loc")


async def test_invalid_enum_value_raises_malformed_output(monkeypatch: pytest.MonkeyPatch) -> None:
    bad = json.dumps({"category": "hacked", "priority": "high", "summary": "x", "confidence": 0.5})
    provider, _ = _make_provider(monkeypatch, bad)
    with pytest.raises(MalformedOutput):
        await provider.triage("text", "loc")


async def test_aclose_closes_the_underlying_client(monkeypatch: pytest.MonkeyPatch) -> None:
    provider, ctor = _make_provider(monkeypatch, VALID_JSON)
    await provider.aclose()
    ctor.return_value.close.assert_awaited_once()
