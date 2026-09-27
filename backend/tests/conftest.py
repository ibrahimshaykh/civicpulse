"""Shared fixtures. No .env file anywhere -- the environment is the only source
of configuration (plan §10.2), so tests set required env vars directly."""

from collections.abc import Iterator

import pytest


@pytest.fixture(scope="session", autouse=True)
def _required_settings_env() -> Iterator[None]:
    """Settings.postgres_password / redis_password have no default (a secret is
    never allowed a default that could ship to a real environment unnoticed).
    Nothing here opens a real connection yet (that lands with DB-02/CA-01), so
    any non-empty value is enough for Settings() to construct.

    Session-scoped (with the module-level `pytest.MonkeyPatch()`, not the
    function-scoped `monkeypatch` fixture) because some test files build the app
    in a module-scoped fixture, which pytest instantiates before any
    function-scoped fixture would have set these env vars.
    """
    mp = pytest.MonkeyPatch()
    mp.setenv("POSTGRES_PASSWORD", "test-only-postgres-password")
    mp.setenv("REDIS_PASSWORD", "test-only-redis-password")
    yield
    mp.undo()
