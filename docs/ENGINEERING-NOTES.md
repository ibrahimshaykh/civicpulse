# Engineering Notes

## Eight Questions

1. **Three things that differ between local dev and CI/prod:**
   - *Network*: local uses `localhost`; Compose uses a Docker bridge (`internal: true` — `compose.yaml:144`); K8s uses cluster-DNS services (`k8s/base/backend.yaml:25`).
   - *Secrets*: local reads from `.env`; CI injects via `POSTGRES_PASSWORD` env var (`compose.yaml:95`); prod uses a K8s Secret manifest (`k8s/base/secret.yaml`).
   - *Filesystem / image freeze*: `backend/Dockerfile:12-17` uses explicit `COPY` layers (not `COPY . .`) so layer caching is deterministic; `compose.prod.yaml:19` pins `image: ghcr.io/.../civicpulse-backend:${IMAGE_TAG:-latest}` instead of using `build:`.

2. **CI/CD Maturity level:** Level 2 — every push to `main` automatically builds and pushes tagged images to GHCR (`.github/workflows/cd.yml`). Next rung is Level 3 (automated canary / blue-green analysis), which buys zero-downtime rollouts with automated rollback on error-rate SLOs.

3. **Build-once-deploy-many:** `compose.prod.yaml:19,24,29,33` replaces `build:` with `image: ghcr.io/.../${IMAGE_TAG:-latest}`, so the same image SHA is promoted through environments without rebuild. The one break risk is front-end config baked at build time rather than injected at runtime.

4. **Deterministic LLM testing:** `SimulatedTriage` (`backend/app/providers/triage/simulated.py:26`) uses a seeded `random.Random` keyed on `seed:sha256(text)` (`simulated.py:49`). CI sets `TRIAGE_PROVIDER=simulated` so no Groq key is needed and results are reproducible across runs.

5. **HPA lag:** Observed ~30–45 s between a load spike and new pods being ready. Delay comes from metric scrape interval (15 s), HPA eval loop (15 s), and pod start time. Mitigated by `stabilizationWindowSeconds: 0` on scale-up (`k8s/base/hpa.yaml:20`) so HPA reacts to the first scrape rather than waiting for a window.

6. **VPA Off mode:** VPA is set to `updateMode: "Off"` (`k8s/base/hpa.yaml:64`). Auto mode would mutate CPU/memory requests live, changing the HPA denominator mid-scale and causing oscillation (HPA scales down while VPA scales up). Off (Recommender-only) lets us read suggestions without automatic mutation.

7. **`internal: true` on the DB network:** `compose.yaml:144` marks the `internal` network with `internal: true`, which means containers on it have no external internet egress. DB and Cache sit only on `internal`; the backend joins both `edge` (for ingress) and `internal` (for DB/Cache — `compose.yaml:117-120`), reaching Groq API via the `edge` network.

8. **The failure:** During week 2, integration tests failed sporadically with `redis.exceptions.ConnectionError`. Root cause: `fakeredis` connections were not being closed between test sessions, leaving file descriptors exhausted. Fixed by adding explicit `await redis.aclose()` in the test fixture teardown (`backend/tests/unit/test_ready_route_unreachable_hosts.py:38`).

## Other Constraints
- **Merge conflict:** Resolved `backend/app/core/config.py` conflict by keeping `groq_max_retries: int = 3` (LLM parameter from one branch) while retaining `db_pool_size: int = 5` (original connection-pool value — `backend/app/core/config.py:26`).
- **Indexes:** `idx_complaints_status` for filtering Dashboard by status; `idx_complaints_created_at` for sorting pagination (see `backend/alembic/versions/0001_*.py`).
- **AOF Volume:** Redis AOF persistence (`compose.yaml:74` redis service `command: --appendonly yes`) ensures rate-limit buckets and triage-cache entries survive a pod restart, preventing quota bursts on restart.
- **Deviations:** `SimulatedTriage` (`backend/app/providers/triage/simulated.py`) was added to allow robust CI testing without real LLM API keys.
