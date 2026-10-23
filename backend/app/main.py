from fastapi import FastAPI

from app.core.config import Settings
from app.core.errors import register_exception_handlers
from app.core.lifecycle import lifespan
from app.core.logging import configure_logging
from app.core.middleware import RequestContextMiddleware
from app.core.openapi import custom_openapi
from app.routes import complaints, health, meta, metrics, stats


def create_app(settings: Settings | None = None) -> FastAPI:
    """Wiring only: settings, logging, middleware, error handlers, routers."""
    s = settings or Settings()
    configure_logging(s.log_level)
    app = FastAPI(
        title="CivicPulse API",
        version=s.app_version,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )
    app.state.settings = s
    app.add_middleware(RequestContextMiddleware)
    register_exception_handlers(app)
    for r in (complaints.router, stats.router, meta.router, health.router, metrics.router):
        app.include_router(r)
    app.openapi = lambda: custom_openapi(app)  # type: ignore[method-assign]
    return app
