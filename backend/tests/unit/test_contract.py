import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.main import create_app

BACKEND = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(create_app())


@pytest.fixture(scope="module")
def schema(client: TestClient) -> dict[str, Any]:
    response = client.get("/api/openapi.json")
    assert response.status_code == 200
    body: dict[str, Any] = response.json()
    return body


def test_openapi_lists_the_contract_endpoints(schema: dict[str, Any]) -> None:
    assert set(schema["paths"]) == {
        "/api/complaints",
        "/api/complaints/{complaint_id}",
        "/api/complaints/{complaint_id}/status",
        "/api/stats",
        "/api/meta/providers",
        "/health",
        "/ready",
    }


def test_openapi_has_no_422_anywhere(schema: dict[str, Any]) -> None:
    for path in schema["paths"].values():
        for op in path.values():
            assert "422" not in op["responses"]
    assert "HTTPValidationError" not in schema["components"]["schemas"]


def test_error_responses_use_the_envelope(schema: dict[str, Any]) -> None:
    patch = schema["paths"]["/api/complaints/{complaint_id}/status"]["patch"]["responses"]
    assert set(patch) == {"200", "400", "404", "409"}
    assert patch["409"]["content"]["application/json"]["schema"] == {"$ref": "#/components/schemas/ErrorBody"}


def test_committed_openapi_json_is_current() -> None:
    exported = subprocess.run(
        [sys.executable, "-m", "app.cli", "export-openapi"],
        cwd=BACKEND,
        capture_output=True,
        check=True,
    ).stdout.decode("utf-8")
    committed = (BACKEND / "openapi.json").read_text(encoding="utf-8")
    assert json.loads(exported) == json.loads(committed), (
        "backend/openapi.json is stale: run `uv run python -m app.cli export-openapi > openapi.json`"
    )


def test_create_returns_201_with_location(client: TestClient) -> None:
    body = json.loads((BACKEND / "tests" / "fixtures" / "complaint_create.json").read_text(encoding="utf-8"))
    response = client.post("/api/complaints", json=body)
    assert response.status_code == 201
    assert response.headers["Location"] == f"/api/complaints/{response.json()['id']}"
    assert response.json()["allowed_transitions"] == ["in_progress", "rejected"]


def test_stats_sets_cache_headers(client: TestClient) -> None:
    response = client.get("/api/stats")
    assert response.status_code == 200
    assert response.headers["X-Cache"] in {"HIT", "MISS"}
    assert response.headers["Cache-Control"] == "no-store"


def test_health_and_metrics(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": "ok"}
    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    assert metrics.headers["content-type"].startswith("text/plain")
