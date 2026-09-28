"""Production entrypoint (task BE-06): `python -m app.server`. Flips
readiness to failing *before* uvicorn starts draining, so a pod stops
receiving new traffic (via `/ready`) as early as possible during a rolling
update -- not just after every in-flight request has already finished.

    t=0    kubelet's preStop hook: sleep 5 (pod still serving; endpoint being removed)
    t~1-3  Service/Ingress stop sending new traffic
    t=5    SIGTERM -> handle_exit -> /ready=503, stop accepting, drain in-flight
    t<=25  drain complete -> lifespan shutdown closes the DB/Redis pools -> exit 0
    t=30   terminationGracePeriodSeconds: SIGKILL if still alive (should never happen)

graceful_timeout_s (20) + preStop (5) < terminationGracePeriodSeconds (30) is
the whole design: BE-06 owns the first two numbers, K8-02 the third.
"""

from types import FrameType

import structlog
import uvicorn

from app.core import lifecycle
from app.core.config import Settings
from app.main import create_app

log = structlog.get_logger()


class GracefulServer(uvicorn.Server):
    def handle_exit(self, sig: int, frame: FrameType | None) -> None:
        lifecycle.shutting_down = True  # before anything else: /ready starts failing immediately
        log.info("shutdown_signal_received", signal=sig)
        super().handle_exit(sig, frame)  # stop accepting, drain in-flight, then run the lifespan shutdown


def main() -> None:
    settings = Settings()
    config = uvicorn.Config(
        create_app(settings),
        host="0.0.0.0",  # noqa: S104 -- the container's only interface; nginx/Ingress sit in front
        port=8000,
        workers=1,  # one process per pod; K8s scales replicas, not in-process workers
        proxy_headers=False,  # deps.client_ip() parses X-Forwarded-For itself, with its own trust boundary
        access_log=False,  # RequestContextMiddleware's structured request_completed log replaces it
        log_config=None,  # keep structlog's JSON formatting; uvicorn's own config would override it
        timeout_graceful_shutdown=settings.graceful_timeout_s,
        lifespan="on",
    )
    GracefulServer(config).run()


if __name__ == "__main__":
    main()
