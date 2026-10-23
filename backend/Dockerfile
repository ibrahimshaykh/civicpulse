# syntax=docker/dockerfile:1
# Multi-stage build: the builder stage has uv + a C toolchain for source
# wheels (asyncpg, lupa's runtime deps); the final image ships neither.

FROM python:3.12-slim AS builder

RUN pip install --no-cache-dir uv==0.5.11

WORKDIR /app

# Dependencies first, so editing app code never invalidates this layer.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

COPY alembic.ini ./
COPY alembic ./alembic
COPY app ./app

# --no-editable would need package=true; this project is package=false
# (backend/pyproject.toml: "an application, not a library"), so the app
# is run straight out of /app with .venv/bin on PATH, same as CI and the
# local `uv run` workflow -- never installed as a wheel.

FROM python:3.12-slim AS runtime

# Upgrade all OS packages to pick up the latest security patches.
# Run as root before switching to app user; clean up apt lists to keep
# the image lean (same pattern as the frontend's apk upgrade).
RUN apt-get update && \
    apt-get upgrade -y --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd --system app && useradd --system --gid app --home-dir /app --shell /usr/sbin/nologin app

WORKDIR /app
COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER app
EXPOSE 8000

# CMD, not ENTRYPOINT+shell: PID 1 is python itself, so SIGTERM reaches
# GracefulServer.handle_exit (BE-06) directly instead of a shell wrapper
# that would swallow it.
CMD ["python", "-m", "app.server"]
