from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

# Fixed rather than taken from the deploy version, so the committed openapi.json
# only changes when the contract does (the CI drift check depends on that).
API_VERSION = "1.0.0"


def custom_openapi(app: FastAPI) -> dict[str, Any]:
    """OpenAPI without FastAPI's automatic 422 entries: we answer validation errors with 400 (plan D7)."""
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(title=app.title, version=API_VERSION, routes=app.routes)
    for path in schema["paths"].values():
        for op in path.values():
            op.get("responses", {}).pop("422", None)
    schemas = schema.get("components", {}).get("schemas", {})
    schemas.pop("HTTPValidationError", None)
    schemas.pop("ValidationError", None)
    app.openapi_schema = schema
    return schema
