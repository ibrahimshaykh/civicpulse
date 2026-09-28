"""Prometheus collectors.

A dedicated registry (not prometheus_client's global default) so tests can
build a fresh app repeatedly without "Duplicated timeseries" errors from
re-registering the same metric names. CA-01, CA-02 and the AI-layer tasks add
their own counters/histograms here as they land -- this file only defines the
ones something currently increments.
"""

from prometheus_client import CollectorRegistry, Counter, Histogram

REGISTRY = CollectorRegistry()

HTTP_REQUESTS = Counter(
    "civicpulse_http_requests_total",
    "HTTP requests by method, route and status",
    ["method", "route", "status"],
    registry=REGISTRY,
)

HTTP_LATENCY = Histogram(
    "civicpulse_http_request_duration_seconds",
    "HTTP request duration by method and route",
    ["method", "route"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
    registry=REGISTRY,
)

RATE_LIMITER_FAIL_OPEN = Counter(
    "civicpulse_rate_limiter_fail_open_total",
    "Times the rate limiter fell back to always-allow because Redis was unavailable",
    registry=REGISTRY,
)
