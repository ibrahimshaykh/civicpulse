# Demo Talking Points — Ibrahim's Ownership Areas

## 1. CI Pipeline (ci.yml)

**What it does:** Runs on every PR to `main`/`dev` and every push to `dev`.

**8 jobs, in order:**

| Job | What it checks |
|-----|---------------|
| `lint-and-type` | Ruff lint + format (backend), mypy types (backend), ESLint + tsc (frontend) |
| `contract` | Re-exports OpenAPI spec → regenerates TS client → `git diff --exit-code` catches drift |
| `status` | Renders `progress.toml` → `STATUS.md`, fails if someone edited STATUS.md by hand |
| `test-backend` | Pytest with real Postgres + Redis (Docker services), simulated triage provider |
| `test-frontend` | Vitest unit tests |
| `integration` | Full Compose stack → Playwright e2e (submit complaint, check dashboard) |
| `image-scan` | Trivy vulnerability scan on the built Docker images |
| `manifest-lint` | `kubeconform` validates all K8s manifests against schemas |

**Key design decisions to mention:**
- `concurrency: cancel-in-progress: true` — newer push kills stale CI run
- `TRIAGE_PROVIDER=simulated` in CI env — deterministic, no API key needed
- `workflow_call: {}` lets cd.yml reuse the entire CI workflow as its test gate
- Contract job catches frontend/backend schema drift before merge

**Evidence:** PR #38 shows red CI (lint + test failures), PR #69 shows all 8 green.

---

## 2. CD Pipeline (cd.yml)

**Trigger:** Push to `main` only (+ manual `workflow_dispatch` for declarative rollback).

**Flow:**
1. Reuses `ci.yml` as a test gate via `workflow_call`
2. Builds Docker images with BuildKit + multi-platform
3. Pushes to GHCR with two tags:
   - `ghcr.io/.../civicpulse-backend:<git-sha>` (deploy target)
   - `ghcr.io/.../civicpulse-backend:latest` (convenience only, never deployed by SHA)
4. Attaches OCI labels (source URL, revision SHA) and SBOM attestation

**Key points:**
- `cancel-in-progress: false` — never cancels a deploy mid-push
- SHA-based tagging = build-once-deploy-many, every deploy is traceable
- `workflow_dispatch` with optional SHA input = declarative rollback without touching the cluster

---

## 3. Kubernetes Manifests (k8s/base/)

**16 resources rendered by `kustomize build`:**

| Resource | Key details |
|----------|------------|
| **Namespace** `civicpulse` | Isolates all resources |
| **ConfigMap** | Non-secret env vars (app_env, log_level, triage_provider, Redis/Postgres hosts) |
| **Secret** (placeholder) | `POSTGRES_PASSWORD`, `REDIS_PASSWORD`, `GROQ_API_KEY` — replaced at deploy time |
| **Postgres StatefulSet** | 1 replica, 5Gi PVC, `PGDATA` on persistent volume |
| **Redis Deployment** | 1 replica, 1Gi PVC, `--requirepass` from secret |
| **Backend Deployment** | 3 probes (startup/liveness/readiness), `preStop` sleep for graceful drain, resource requests/limits |
| **Frontend Deployment** | Nginx serving the built React app |
| **Services** | ClusterIP for backend (:8000) and frontend (:80) |
| **Ingress** (Traefik) | `/api` → backend, `/` → frontend |

### HPA Configuration (autoscaling/v2)
- Target: backend Deployment
- Range: 2–6 replicas
- Metric: CPU at 70% average utilization
- **Scale-up behavior:** stabilization 0s (react immediately), can double pods every 30s
- **Scale-down behavior:** stabilization 300s (5 min cooldown), removes 1 pod per 60s max
- *Why asymmetric:* scale up fast for traffic spikes, scale down slowly to avoid flapping

### PodDisruptionBudgets
- `backend` PDB: `minAvailable: 1` — at least 1 pod stays up during voluntary disruptions
- `frontend` PDB: `minAvailable: 1` — same guarantee for the frontend

### VPA (Off Mode)
- `updateMode: "Off"` = recommendation-only, never auto-adjusts resource requests
- *Why Off:* needs VPA CRDs + recommender add-on installed; we ship the manifest so the config is in-repo ready to activate. Full guess→load→recommend→update loop (K8-06) needs a real 10+ min load test per iteration — out of scope for this sprint
- Once activated, it would recommend CPU/memory requests based on observed usage

### Rollback Procedure
**Imperative (instant):**
```bash
kubectl -n civicpulse rollout undo deployment/backend
kubectl -n civicpulse rollout status deployment/backend
```

**Declarative (GitOps-friendly):**
```bash
# Revert the image tag in kustomization.yaml (or git revert the bump commit)
kubectl apply -k k8s/overlays/prod
```

**Via CD pipeline:** Trigger `workflow_dispatch` on cd.yml with the old commit SHA — rebuilds nothing, just re-deploys the existing image.

---

## 4. AI Layer — TriageProvider Architecture

### The Interface (Protocol pattern)
```python
class TriageProvider(Protocol):
    async def triage(self, text: str, location: str) -> TriageResult
```
- `TriageResult`: frozen Pydantic model with `category`, `priority`, `summary`, `confidence`
- Every provider implements this one method — swap providers without touching callers

### Four Providers

| Provider | `TRIAGE_PROVIDER=` | How it works |
|----------|-------------------|-------------|
| **GroqTriage** | `llm` | Calls Groq API (OpenAI-compatible), Llama 3.1 8B, JSON mode, temp=0 |
| **OllamaTriage** | `ollama` | Same prompt, local Ollama server, Llama 3.2 1B |
| **RuleBasedTriage** | `rules` | Deterministic keyword matching — 5 categories × ~10 keywords each, HIGH_RISK escalation list |
| **SimulatedTriage** | `simulated` | Seeded random for CI — deterministic, no network calls |

### Fallback Chain (TriageService)
```
Primary provider (e.g. Groq)
  → timeout/error? → 1 jittered retry
    → still fails? → RuleBasedTriage fallback (always available)
```
- `build_triage_service()` wires: primary + fallback + cache + outcome log
- Retryable errors: `TimeoutError`, `APIConnectionError`, `RateLimitError`, `InternalServerError`
- Non-retryable: bad request, auth failure, `MalformedOutput` — fall straight through to rules

### Safety Features
- **PII Redaction** (`redaction.py`): strips Pakistani mobile numbers, CNIC, email, house addresses before text reaches LLM — regex patterns with `[PHONE]`, `[CNIC]`, `[EMAIL]`, `[ADDRESS]` replacements
- **Content-hash Cache** (`cache.py`): SHA-256 of normalized text + provider + model + prompt version → Redis key, 24h TTL. Nine identical complaints = one Groq call. Hit/miss counters in Redis (not in-process) so they aggregate across all backend pods
- **Safety Floor** (`TriageService`): if LLM confidence < threshold or returns nonsensical category, rules provider backstops
- **Prompt Injection Guard**: text normalization + structured JSON output mode limits attack surface

### Key Design Decisions to Mention
- `max_retries=0` on the OpenAI SDK client — TriageService owns the retry budget, not the SDK (prevents silent 3x amplification)
- Location is deliberately excluded from the cache key — same complaint text from different addresses should cost one API call
- `MappingProxyType` on the keyword table — runtime mutation of shared config is impossible
- `reporter_contact` and `location` never sent to LLM (ADR 0004) — only the redacted complaint text
