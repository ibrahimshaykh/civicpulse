import json

from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app


def test_u8_validation_error_becomes_400_with_text_field(monkeypatch: object) -> None:
    client = TestClient(create_app())
    response = client.post("/api/complaints", json={"text": "short", "location": "Real Street 12"})
    assert response.status_code == 400
    body = response.json()
    assert body["error"]["code"] == "validation_error"
    assert any(f["field"] == "text" for f in body["error"]["fields"])
    # "body"/"query"/"path" is where the error came from, not part of the name.
    assert not any(f["field"].startswith(("body.", "query.", "path.")) for f in body["error"]["fields"])


def test_u10_settings_repr_hides_passwords_and_api_keys() -> None:
    settings = Settings(
        postgres_password="super-secret-pg-password",
        redis_password="super-secret-redis-password",
        groq_api_key="gsk_totally_real_looking_key",
    )
    rendered = repr(settings)
    assert "super-secret-pg-password" not in rendered
    assert "super-secret-redis-password" not in rendered
    assert "gsk_totally_real_looking_key" not in rendered
    # database_url is a computed field that assembles the DSN *with* the real
    # password in it -- repr=False keeps it out of repr() entirely (plan §10.2).
    assert "database_url" not in rendered


def test_i15_request_id_echoed_generated_and_logged(capsys: object) -> None:
    # Fresh app built here (not the module-scoped client some other test file
    # uses) so configure_logging() picks up capsys's already-redirected stdout.
    client = TestClient(create_app())

    provided = "caller-supplied-id-123"
    response = client.get("/api/complaints", headers={"X-Request-ID": provided})
    assert response.headers["X-Request-ID"] == provided

    response2 = client.get("/api/complaints")
    generated = response2.headers["X-Request-ID"]
    assert generated != "-"
    assert generated != provided

    out = capsys.readouterr().out  # type: ignore[attr-defined]
    lines = [json.loads(line) for line in out.splitlines() if line.strip()]
    request_ids_logged = {
        line.get("request_id") for line in lines if line.get("event") == "request_completed"
    }
    assert provided in request_ids_logged
    assert generated in request_ids_logged
