from fastapi import FastAPI

from app.core.openapi import custom_openapi
from app.routes import complaints, health, meta, metrics, stats


def create_app() -> FastAPI:
    """Wiring only. BE-01 adds settings, logging, middleware and the 400 error handlers."""
    app = FastAPI(title="CivicPulse API", docs_url="/api/docs", openapi_url="/api/openapi.json")
    for r in (complaints.router, stats.router, meta.router, health.router, metrics.router):
        app.include_router(r)
    app.openapi = lambda: custom_openapi(app)  # type: ignore[method-assign]
    return app
