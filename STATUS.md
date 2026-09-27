# CivicPulse — status

> Generated from `docs/progress.toml` by `python scripts/update_status.py`. Edit the TOML, then regenerate. Don't edit this file by hand.
> Last updated: 2026-09-27

```text
Project progress  [██████░░░░░░░░░░░░░░░░░░░░░░░░]   20%   18 of 87 core tasks done
Marks secured     [████░░░░░░░░░░░░░░░░░░░░░░░░░░]   14%   22.3 of 150 marks  (26 of 175 rubric points)
```

> ⚠️ The brief's rubric sections add up to **175** points but its header says **150** marks. Marks above are scaled ×150/175 until the instructor confirms. If the real total is 175, set `total_marks = 175` in `docs/progress.toml`.

Bonus secured: **0 of 15**. Marks are self-assessed and count a rubric line only when every task it needs is done. The final grade also applies the viva multiplier and the brief's automatic deductions.

| Partner | Core tasks done | Share of core tasks |
|---|---|---|
| Partner A (frontend, backend, data) | 17 of 37 | `████░░░░░░` 45% |
| Partner B (AI layer, DevOps) | 1 of 39 | `░░░░░░░░░░` 2% |
| Shared tasks | 0 of 11 | `░░░░░░░░░░` 0% |

## Marks by rubric section

Raw rubric points, as printed in the brief.

| Section | Secured | Out of | |
|---|---:|---:|---|
| A · Collaboration and version control | 0 | 15 | `░░░░░░░░░░` |
| B · Frontend | 13 | 18 | `███████░░░` |
| C · Backend | 3 | 25 | `█░░░░░░░░░` |
| D · Data layer | 10 | 12 | `████████░░` |
| E · Cache layer | 0 | 10 | `░░░░░░░░░░` |
| F · AI layer | 0 | 25 | `░░░░░░░░░░` |
| G · Docker and Compose | 0 | 15 | `░░░░░░░░░░` |
| H · Kubernetes | 0 | 20 | `░░░░░░░░░░` |
| I · CI/CD | 0 | 20 | `░░░░░░░░░░` |
| J · Documentation | 0 | 15 | `░░░░░░░░░░` |
| **Total** | **26** | **175** | `█░░░░░░░░░` |

## Working on now

- 🔄 **C0-01** GitHub repo first: push plan + STATUS, dev branch, protection, templates, CODEOWNERS (A)

## Needs you

- [ ] Add SalmanAsadDev as a collaborator (Settings -> Collaborators -> Add people); he must accept the invite before he can push or review. _(needed for C0-01)_
- [ ] Ask Salman to connect his own Claude Code session to his own GitHub account (or at minimum run git with his own name/email), so his tasks commit as him, not through this session. _(needed for C0-01)_
- [ ] Before turning in: make the repo public, or add both instructors as collaborators. _(needed for SUB-03)_
- [ ] Ask the instructor which endpoint is the 'tenth' (plan §1.3) and note the answer. _(needed for C0-05)_
- [ ] Ask the instructor: the rubric sections add up to 175, but the header says 150. Is it scaled to 150 or out of 175?
- [ ] Week 2: create a Groq API key; it goes only in your local .env and in GitHub Secrets, never in the repo. _(needed for AI-04)_

## Up next

**Partner A (frontend, backend, data)**

- ⬜ **C0-09** Deliberate merge conflict on config.py, resolved and justified — Claude builds, you run it (week 2)
- ⬜ **FE-11** nginx runtime config template, frontend Dockerfile, .dockerignore — Claude builds, you run it (week 2)
- ⬜ **DB-04** EXPLAIN evidence for both indexes at 200k rows — Claude (week 2)
- ⬜ **BE-02** Repositories and unit of work — Claude (week 2)

**Partner B (AI layer, DevOps)**

- ⬜ **C0-04** Freeze TriageProvider / TriageResult / TriageOutcome seam — Claude (week 1)
- ⬜ **AI-01** RuleBasedTriage + tests — Claude (week 1)
- ⬜ **AI-02** SimulatedTriage with failure injection — Claude (week 1)
- ⬜ **AI-03** TriageService skeleton + fallback + the fallback test — Claude (week 1)

## Hands-on work for you and your partner

Claude does every task marked "Claude". These are the ones that need a person. Claude gives step-by-step instructions for each one when it comes up.

| Week | Task | Who | What you do |
|---:|---|---|---|
| 1 | 🔄 **C0-01** GitHub repo first: push plan + STATUS, dev branch, protection, templates, CODEOWNERS | Claude builds, you run it | Create the repo (or connect GitHub), add your partner, turn on branch protection |
| 1 | ⬜ **DK-01** Backend multi-stage non-root Dockerfile | Claude builds, you run it | Run the commands Claude gives, paste the output back |
| 1 | ⬜ **DK-02** .dockerignore per context + before/after sizes | Claude builds, you run it | Run the commands Claude gives, paste the output back |
| 1 | ⬜ **DK-03** compose.yaml data tier, internal network, AOF volume | Claude builds, you run it | Run the commands Claude gives, paste the output back |
| 2 | ⬜ **C0-09** Deliberate merge conflict on config.py, resolved and justified | Claude builds, you run it | You and your partner each commit one side from your own accounts, then screenshot |
| 2 | ⬜ **FE-11** nginx runtime config template, frontend Dockerfile, .dockerignore | Claude builds, you run it | Run the commands Claude gives, paste the output back |
| 2 | ⬜ **AI-04** Groq provider, JSON mode, strict output validation | Claude builds, you run it | Create a Groq key, put it in .env only, run one live call |
| 2 | ⬜ **AI-08** Content-hash triage cache + measured hit rate | Claude builds, you run it | Run the hit-rate replay with your Groq key and paste the numbers |
| 2 | ⬜ **DK-04** migrate + seed services, healthchecks, make up | Claude builds, you run it | Run the commands Claude gives, paste the output back |
| 2 | ⬜ **CI-07** Required status checks wired into branch protection | you, step by step | All of it, following Claude's steps |
| 2 | ⬜ **EV-03** Merge conflict markers / resolution / merge screenshots | you, step by step | All of it, following Claude's steps |
| 3 | ⬜ **FE-12** Switch from MSW to the real API, fix contract mismatches | Claude builds, you run it | Run the commands Claude gives, paste the output back |
| 3 | ⬜ **AI-09** Ollama provider, offline profile, warm-up | Claude builds, you run it | Install Ollama's model via make offline and paste the latency numbers |
| 3 | ⬜ **DK-05** compose.prod.yaml (image by tag, no build, no DB/cache ports) | Claude builds, you run it | Run the commands Claude gives, paste the output back |
| 3 | ⬜ **DK-06** Offline profile with ollama_models volume | Claude builds, you run it | Run the commands Claude gives, paste the output back |
| 3 | ⬜ **DK-07** Image size report (build stage vs final) | Claude builds, you run it | Run the commands Claude gives, paste the output back |
| 3 | ⬜ **K8-01** k3d cluster, namespace, ConfigMap, placeholder Secret, Postgres StatefulSet, Redis | Claude builds, you run it | Run the commands Claude gives, paste the output back |
| 3 | ⬜ **K8-02** Backend/frontend Deployments: three probes, preStop, requests/limits | Claude builds, you run it | Run the commands Claude gives, paste the output back |
| 3 | ⬜ **K8-03** ClusterIP Services + Ingress for / and /api | Claude builds, you run it | Run the commands Claude gives, paste the output back |
| 3 | ⬜ **K8-04** HPA v2 with behavior, PDB, VPA (Off) | Claude builds, you run it | Run the commands Claude gives, paste the output back |
| 3 | ⬜ **DOC-09** TRIAGE.md: prompt, latency, accuracy, hit rate | Claude builds, you run it | Run the benchmark with your Groq key and paste the output |
| 3 | ⬜ **EV-02** 5+ merged PRs linked to Issues with substantive reviews | your partner | Your partner does it from his own account |
| 4 | ⬜ **DB-05** Persistence demos (Compose and Kubernetes) | you, step by step | All of it, following Claude's steps |
| 4 | ⬜ **K8-05** k6 load test, hpa -w capture, replicas-vs-load chart, lag analysis | Claude builds, you run it | Run the commands Claude gives, paste the output back |
| 4 | ⬜ **K8-06** VPA loop: guess, load, recommend, update requests, re-test | Claude builds, you run it | Run the commands Claude gives, paste the output back |
| 4 | ⬜ **K8-08** Rollback, imperative and declarative | Claude builds, you run it | Run the commands Claude gives, paste the output back |
| 4 | ⬜ **CI-05** Ephemeral k3d deploy job, rollout status, Ingress smoke test | Claude builds, you run it | Add the three repository secrets in GitHub settings |
| 4 | ⬜ **DOC-01** README with badges, Mermaid, quickstart, API table, screenshots | Claude builds, you run it | Take the screenshots Claude lists; test the quickstart on another machine |
| 4 | ⬜ **DOC-07** ENGINEERING-NOTES: eight answers + conflict, indexes, AOF, deviations | Claude builds, you run it | Tell Claude your real Q8 failure story; check every answer is true |
| 4 | ⬜ **DOC-08** AI-USAGE.md | Claude builds, you run it | Confirm the AI-USAGE account of what Claude wrote is accurate |
| 4 | ⬜ **DOC-10** Demo video (<= 5 min, both partners) | you, step by step | All of it, following Claude's steps |
| 4 | ⬜ **EV-04** Commit audit: 35+ conventional commits, both partners >= 35% | Claude builds, you run it | Run git shortlog -sn --no-merges and paste the output |
| 4 | ⬜ **EV-05** Persistence transcripts | you, step by step | All of it, following Claude's steps |
| 4 | ⬜ **EV-06** Network isolation transcript | you, step by step | All of it, following Claude's steps |
| 4 | ⬜ **EV-07** Red PR blocked, then green | Claude builds, you run it | Screenshot the red PR with merge blocked, then the green one |
| 4 | ⬜ **SUB-01** check_submission.py clean, clean-clone quickstart tested elsewhere | Claude builds, you run it | Run check_submission.py and paste the output; clone on a second machine and run make up |
| 4 | ⬜ **SUB-02** Tag v1.0.0 (release.yml retags the deployed SHA) | Claude builds, you run it | Run git tag v1.0.0 and git push --tags (Claude does it if GitHub is connected) |
| 4 | ⬜ **SUB-03** Instructor access: repo public, or both instructors added as collaborators | you, step by step | All of it, following Claude's steps |
| 4 | ⬜ **SUB-04** Turn in the six items on the course portal (brief §5.8) | you, step by step | All of it, following Claude's steps |
| 4 | ⬜ **K8-07** Zero-downtime rollout under live load ⭐ | Claude builds, you run it | Run the commands Claude gives, paste the output back |
| 4 | ⬜ **OB-01** Prometheus + Grafana dashboard ⭐ | Claude builds, you run it | Run the commands Claude gives, paste the output back |
| 4 | ⬜ **OB-03** GitOps with Argo CD or Flux ⭐ | Claude builds, you run it | Run the commands Claude gives, paste the output back |

## Submission portal checklist

The portal takes these items (brief §5.8), not files. Every file lives in the GitHub repo.

**0 of 8 ready.**

- ⬜ Before turning in: check_submission.py runs clean — waiting on SUB-01
- 🔄 GitHub repository URL (public, or private with both instructors added) — waiting on C0-01, SUB-03
- ⬜ Link to a successful cd.yml run that tested, published and deployed — waiting on CI-04, CI-05
- ⬜ Links to both GHCR images showing SHA tags — waiting on CI-04
- ⬜ Demo video link (unlisted) — waiting on DOC-10
- ⬜ git shortlog -sn output, pasted — waiting on EV-04
- ⬜ kubectl get hpa -w capture and the replicas-vs-load chart — waiting on K8-05
- ⬜ Turned in on the portal — waiting on SUB-04

## Built

| Done on | Task | Owner |
|---|---|---|
| 2026-09-27 | **EV-01** Branch protection screenshot | B |
| 2026-09-27 | **BE-01** Settings, JSON logging, request-id middleware, error handlers | A |
| 2026-09-27 | **DB-03** Idempotent seed CLI with 33 complaints | A |
| 2026-09-27 | **DB-02** Alembic async env with advisory lock, migration 0001 | A |
| 2026-09-27 | **DB-01** SQLAlchemy base, naming convention, ORM model | A |
| 2026-09-27 | **FE-09** Stats view: aggregates, X-Cache indicator, providers panel | A |
| 2026-09-27 | **FE-08** Dashboard: server-driven transitions, verbatim 409 | A |
| 2026-09-27 | **FE-07** Dashboard: table, URL filters, pagination | A |
| 2026-09-27 | **FE-06** Submit view: 400 field mapping, 429 countdown, network errors | A |
| 2026-09-27 | **FE-05** Submit view: form, zod validation, honest loading, result ticket | A |
| 2026-09-27 | **FE-04** Router, layout, nav rail, error boundary | A |
| 2026-09-27 | **FE-03** MSW handlers and typed fixtures | A |
| 2026-09-27 | **FE-02** Typed API client generated from OpenAPI + drift script | A |
| 2026-09-27 | **FE-01** Vite + React + TS strict scaffold, Tailwind, ESLint, exact versions | A |
| 2026-09-27 | **C0-05** Stub routes and committed openapi.json | A |
| 2026-09-27 | **C0-03** Backend pyproject, uv lockfile, ruff, mypy | A |
| 2026-09-27 | **C0-02** Domain enums and Pydantic schemas | A |
| 2026-09-27 | **C0-00** Implementation plan and progress tracker | A |

<details>
<summary><strong>Every rubric line and what it still needs</strong></summary>

| Line | Marks | State | Still needed |
|---|---:|---|---|
| A1 main protected, PR + CI + approval required, screenshot | 3 | 🔄 | C0-01, CI-07 |
| A2 dev + feature branches, nothing committed directly to main | 2 | 🔄 | C0-01, EV-04 |
| A3 >= 5 merged PRs, each linked to an Issue, substantive partner review | 4 | ⬜ | EV-02 |
| A4 >= 35 conventional commits, neither partner below 35% | 3 | ⬜ | EV-04 |
| A5 Deliberate merge conflict with evidence and justification | 3 | ⬜ | C0-09, EV-03 |
| B1 Submit view: validation, honest loading, category/priority/summary/provider | 5 | ✅ | — |
| B2 Dashboard: pagination, filters, transitions, verbatim 409 | 5 | ✅ | — |
| B3 Stats view with aggregates and X-Cache state | 3 | ✅ | — |
| B4 Runtime configuration, one image for every environment | 3 | ⬜ | FE-11 |
| B5 >= 5 meaningful component tests passing in CI | 2 | ⬜ | FE-10, CI-01 |
| C1 All ten endpoints to contract, correct codes, field-level errors | 7 | 🔄 | BE-03, BE-04, BE-05, CA-01, AI-10, FE-12 |
| C2 Four-layer separation | 4 | ⬜ | BE-02, BE-08 |
| C3 Explicit transition table, invalid transitions 409 | 3 | ⬜ | BE-04 |
| C4 /health vs /ready, /health never touches the DB | 3 | ⬜ | BE-05 |
| C5 Structured JSON logs with propagated request_id | 3 | ✅ | — |
| C6 SIGTERM drains in-flight requests | 2 | ⬜ | BE-06 |
| C7 >= 14 deterministic tests, coverage >= 65% | 3 | ⬜ | BE-07, CI-01 |
| D1 Alembic migrations, no DDL at startup | 4 | ✅ | — |
| D2 Complete schema incl. triaged_by, ai_summary, latency, timestamptz | 3 | ✅ | — |
| D3 Two indexes, each justified by a named query | 2 | ⬜ | DB-04, DOC-07 |
| D4 Idempotent seed of >= 30 complaints | 3 | ✅ | — |
| E1 /api/stats read-through cache, 30 s TTL, X-Cache | 3 | ⬜ | CA-01 |
| E2 Invalidated on write | 2 | ⬜ | CA-01 |
| E3 Distributed Redis rate limiter, 429 + Retry-After | 4 | ⬜ | CA-02 |
| E4 Redis AOF on a named volume, justified | 1 | ⬜ | DK-03, DOC-07 |
| F1 TriageProvider with >= 3 implementations selected by env var | 5 | ⬜ | AI-01, AI-02, AI-04, AI-11 |
| F2 Structured output validated by Pydantic, malformed rejected safely | 5 | ⬜ | AI-04 |
| F3 Timeout, single jittered retry, fallback, triaged_by recorded | 6 | ⬜ | AI-03, AI-05 |
| F4 Content-hash cache with measured, reported hit rate | 3 | ⬜ | AI-08, DOC-09 |
| F5 Prompt-injection guardrail + injection test | 3 | ⬜ | AI-06 |
| F6 triage_latency_ms surfaced via /api/meta/providers | 2 | ⬜ | AI-10 |
| F7 PII / data-governance ADR | 1 | ⬜ | AI-07, DOC-05 |
| G1 Both images multi-stage, pinned, non-root, exec CMD, cache-correct | 4 | ⬜ | DK-01, FE-11 |
| G2 .dockerignore per context with before/after sizes | 2 | ⬜ | DK-02 |
| G3 Two networks, internal: true, frontend provably can't reach DB | 4 | ⬜ | DK-03, EV-06 |
| G4 Three named volumes justified, dev bind mount only in dev | 2 | ⬜ | DK-04, DK-06 |
| G5 Healthchecks + depends_on service_healthy | 2 | ⬜ | DK-04 |
| G6 compose.prod.yaml: image tag, no build, no DB/cache port | 1 | ⬜ | DK-05 |
| H1 Namespace, Deployments, StatefulSet + PVC, ClusterIP, Ingress / and /api | 5 | ⬜ | K8-01, K8-02, K8-03 |
| H2 ConfigMap and Secret separated, placeholders only | 2 | ⬜ | K8-01 |
| H3 Three probes wired correctly | 4 | ⬜ | K8-02 |
| H4 requests and limits on every container | 2 | ⬜ | K8-02 |
| H5 HPA v2 with behavior, hpa -w capture, replicas-vs-load chart | 4 | ⬜ | K8-04, K8-05 |
| H6 VPA recommender, requests updated, conflict explained | 3 | ⬜ | K8-04, K8-06 |
| I1 ci.yml lint, types, tests on every PR, required checks | 4 | ⬜ | CI-01, CI-07 |
| I2 Compose integration smoke job | 3 | ⬜ | CI-02 |
| I3 Trivy + kubeconform in CI | 3 | ⬜ | CI-03 |
| I4 cd.yml needs-gated, GHCR images tagged by SHA | 4 | ⬜ | CI-04, CI-06 |
| I5 Ephemeral cluster deploy, rollout status, Ingress smoke test | 3 | ⬜ | CI-05 |
| I6 GitHub Secrets, scoped token, least-privilege permissions | 2 | ⬜ | CI-04, CI-05 |
| I7 Red pipeline blocking a merge, then green | 1 | ⬜ | EV-07 |
| J1 README: problem, badges, Mermaid, quickstart, API table, screenshots | 4 | ⬜ | DOC-01 |
| J2 Four ADRs | 4 | ⬜ | DOC-02, DOC-03, DOC-04, DOC-05 |
| J3 RUNBOOK | 2 | ⬜ | DOC-06 |
| J4 Demo video <= 5 min, both partners, all six segments | 3 | ⬜ | DOC-10, K8-08 |
| J5 ENGINEERING-NOTES answering all eight questions with file:line refs | 2 | ⬜ | DOC-07 |
| X1 ⭐ Zero-downtime rolling update under live load | +4 | ⬜ | K8-07 |
| X2 ⭐ GitOps with Argo CD or Flux | +4 | ⬜ | OB-03 |
| X3 ⭐ Deploy by digest with Cosign sign + verify | +3 | ⬜ | CI-08 |
| X4 ⭐ Prometheus + Grafana, screenshot committed | +2 | ⬜ | OB-01 |
| X5 ⭐ OpenTelemetry frontend -> backend -> LLM | +2 | ⬜ | OB-02 |

</details>

<details>
<summary><strong>All tasks by phase</strong></summary>

**Setup and contract** — 4 of 7 done

- ✅ C0-00 Implementation plan and progress tracker (A, Claude, week 1)
- 🔄 C0-01 GitHub repo first: push plan + STATUS, dev branch, protection, templates, CODEOWNERS (A, Claude builds, you run it, week 1)
- ✅ C0-02 Domain enums and Pydantic schemas (A, Claude, week 1)
- ✅ C0-03 Backend pyproject, uv lockfile, ruff, mypy (A, Claude, week 1)
- ⬜ C0-04 Freeze TriageProvider / TriageResult / TriageOutcome seam (B, Claude, week 1)
- ✅ C0-05 Stub routes and committed openapi.json (A, Claude, week 1)
- ⬜ C0-09 Deliberate merge conflict on config.py, resolved and justified (Both, Claude builds, you run it, week 2)

**Frontend** — 9 of 12 done

- ✅ FE-01 Vite + React + TS strict scaffold, Tailwind, ESLint, exact versions (A, Claude, week 1)
- ✅ FE-02 Typed API client generated from OpenAPI + drift script (A, Claude, week 1)
- ✅ FE-03 MSW handlers and typed fixtures (A, Claude, week 1)
- ✅ FE-04 Router, layout, nav rail, error boundary (A, Claude, week 1)
- ✅ FE-05 Submit view: form, zod validation, honest loading, result ticket (A, Claude, week 1)
- ✅ FE-06 Submit view: 400 field mapping, 429 countdown, network errors (A, Claude, week 1)
- ✅ FE-07 Dashboard: table, URL filters, pagination (A, Claude, week 2)
- ✅ FE-08 Dashboard: server-driven transitions, verbatim 409 (A, Claude, week 2)
- ✅ FE-09 Stats view: aggregates, X-Cache indicator, providers panel (A, Claude, week 2)
- ⬜ FE-10 Component test suite (12 tests) passing in CI (B, Claude, week 2)
- ⬜ FE-11 nginx runtime config template, frontend Dockerfile, .dockerignore (A, Claude builds, you run it, week 2)
- ⬜ FE-12 Switch from MSW to the real API, fix contract mismatches (A, Claude builds, you run it, week 3)

**Data layer** — 3 of 5 done

- ✅ DB-01 SQLAlchemy base, naming convention, ORM model (A, Claude, week 2)
- ✅ DB-02 Alembic async env with advisory lock, migration 0001 (A, Claude, week 2)
- ✅ DB-03 Idempotent seed CLI with 33 complaints (A, Claude, week 2)
- ⬜ DB-04 EXPLAIN evidence for both indexes at 200k rows (A, Claude, week 2)
- ⬜ DB-05 Persistence demos (Compose and Kubernetes) (A, you, step by step, week 4)

**Backend** — 1 of 8 done

- ✅ BE-01 Settings, JSON logging, request-id middleware, error handlers (A, Claude, week 2)
- ⬜ BE-02 Repositories and unit of work (A, Claude, week 2)
- ⬜ BE-03 Complaint service + create/get/list routes (A, Claude, week 3)
- ⬜ BE-04 State machine table, PATCH status, race guard (A, Claude, week 3)
- ⬜ BE-05 /health, /ready, /metrics (A, Claude, week 3)
- ⬜ BE-06 SIGTERM graceful server and lifespan (A, Claude, week 3)
- ⬜ BE-07 Backend test suite (30+ tests, coverage >= 70%) (A, Claude, week 3)
- ⬜ BE-08 Architecture test, ruff banned-api, OpenAPI 400 cleanup (A, Claude, week 3)

**Cache** — 0 of 2 done

- ⬜ CA-01 Stats read-through cache, X-Cache, invalidation on write (A, Claude, week 3)
- ⬜ CA-02 Distributed Redis rate limiter, 429 + Retry-After (A, Claude, week 3)

**AI layer** — 0 of 11 done

- ⬜ AI-01 RuleBasedTriage + tests (B, Claude, week 1)
- ⬜ AI-02 SimulatedTriage with failure injection (B, Claude, week 1)
- ⬜ AI-03 TriageService skeleton + fallback + the fallback test (B, Claude, week 1)
- ⬜ AI-04 Groq provider, JSON mode, strict output validation (B, Claude builds, you run it, week 2)
- ⬜ AI-05 10 s timeout + single jittered retry on retryable errors only (B, Claude, week 2)
- ⬜ AI-06 Prompt, injection guardrail, safety floor, injection test (B, Claude, week 2)
- ⬜ AI-07 PII redaction (feeds ADR 0004) (B, Claude, week 2)
- ⬜ AI-08 Content-hash triage cache + measured hit rate (B, Claude builds, you run it, week 2)
- ⬜ AI-09 Ollama provider, offline profile, warm-up (B, Claude builds, you run it, week 3)
- ⬜ AI-10 Outcome ring buffer + /api/meta/providers (B, Claude, week 3)
- ⬜ AI-11 Provider factory selected by TRIAGE_PROVIDER (B, Claude, week 3)

**Docker and Compose** — 0 of 7 done

- ⬜ DK-01 Backend multi-stage non-root Dockerfile (B, Claude builds, you run it, week 1)
- ⬜ DK-02 .dockerignore per context + before/after sizes (B, Claude builds, you run it, week 1)
- ⬜ DK-03 compose.yaml data tier, internal network, AOF volume (B, Claude builds, you run it, week 1)
- ⬜ DK-04 migrate + seed services, healthchecks, make up (B, Claude builds, you run it, week 2)
- ⬜ DK-05 compose.prod.yaml (image by tag, no build, no DB/cache ports) (B, Claude builds, you run it, week 3)
- ⬜ DK-06 Offline profile with ollama_models volume (B, Claude builds, you run it, week 3)
- ⬜ DK-07 Image size report (build stage vs final) (Both, Claude builds, you run it, week 3)

**Kubernetes** — 0 of 8 done

- ⬜ K8-01 k3d cluster, namespace, ConfigMap, placeholder Secret, Postgres StatefulSet, Redis (B, Claude builds, you run it, week 3)
- ⬜ K8-02 Backend/frontend Deployments: three probes, preStop, requests/limits (B, Claude builds, you run it, week 3)
- ⬜ K8-03 ClusterIP Services + Ingress for / and /api (B, Claude builds, you run it, week 3)
- ⬜ K8-04 HPA v2 with behavior, PDB, VPA (Off) (B, Claude builds, you run it, week 3)
- ⬜ K8-05 k6 load test, hpa -w capture, replicas-vs-load chart, lag analysis (B, Claude builds, you run it, week 4)
- ⬜ K8-06 VPA loop: guess, load, recommend, update requests, re-test (B, Claude builds, you run it, week 4)
- ⬜ K8-08 Rollback, imperative and declarative (B, Claude builds, you run it, week 4)
- ⬜ K8-07 Zero-downtime rollout under live load (B, Claude builds, you run it, week 4) ⭐

**CI/CD** — 0 of 8 done

- ⬜ CI-01 ci.yml: lint, types, contract, status, tests (B, Claude, week 1)
- ⬜ CI-02 Compose integration smoke job (MISS then HIT) (B, Claude, week 3)
- ⬜ CI-03 Image build, Trivy scan, kubeconform (B, Claude, week 3)
- ⬜ CI-04 cd.yml: needs-gated GHCR push by SHA, SBOM, least-privilege permissions (B, Claude, week 3)
- ⬜ CI-05 Ephemeral k3d deploy job, rollout status, Ingress smoke test (B, Claude builds, you run it, week 4)
- ⬜ CI-06 release.yml retagging the SHA image on v* tags (B, Claude, week 4)
- ⬜ CI-07 Required status checks wired into branch protection (B, you, step by step, week 2)
- ⬜ CI-08 Deploy by digest, Cosign sign and verify, SHA-pinned actions (B, Claude, week 4) ⭐

**Documentation** — 0 of 10 done

- ⬜ DOC-01 README with badges, Mermaid, quickstart, API table, screenshots (Both, Claude builds, you run it, week 4)
- ⬜ DOC-02 ADR 0001 provider interface (B, Claude, week 4)
- ⬜ DOC-03 ADR 0002 frontend runtime config (A, Claude, week 4)
- ⬜ DOC-04 ADR 0003 deploy by SHA (B, Claude, week 4)
- ⬜ DOC-05 ADR 0004 PII and data governance (B, Claude, week 2)
- ⬜ DOC-06 RUNBOOK: deploy, roll back, logs, triage failing (Both, Claude, week 4)
- ⬜ DOC-07 ENGINEERING-NOTES: eight answers + conflict, indexes, AOF, deviations (Both, Claude builds, you run it, week 4)
- ⬜ DOC-08 AI-USAGE.md (Both, Claude builds, you run it, week 4)
- ⬜ DOC-09 TRIAGE.md: prompt, latency, accuracy, hit rate (B, Claude builds, you run it, week 3)
- ⬜ DOC-10 Demo video (<= 5 min, both partners) (Both, you, step by step, week 4)

**Evidence** — 1 of 7 done

- ✅ EV-01 Branch protection screenshot (B, you, step by step, week 1)
- ⬜ EV-02 5+ merged PRs linked to Issues with substantive reviews (Both, your partner, week 3)
- ⬜ EV-03 Merge conflict markers / resolution / merge screenshots (Both, you, step by step, week 2)
- ⬜ EV-04 Commit audit: 35+ conventional commits, both partners >= 35% (A, Claude builds, you run it, week 4)
- ⬜ EV-05 Persistence transcripts (A, you, step by step, week 4)
- ⬜ EV-06 Network isolation transcript (A, you, step by step, week 4)
- ⬜ EV-07 Red PR blocked, then green (B, Claude builds, you run it, week 4)

**Submission** — 0 of 4 done

- ⬜ SUB-01 check_submission.py clean, clean-clone quickstart tested elsewhere (Both, Claude builds, you run it, week 4)
- ⬜ SUB-02 Tag v1.0.0 (release.yml retags the deployed SHA) (Both, Claude builds, you run it, week 4)
- ⬜ SUB-03 Instructor access: repo public, or both instructors added as collaborators (A, you, step by step, week 4)
- ⬜ SUB-04 Turn in the six items on the course portal (brief §5.8) (A, you, step by step, week 4)

**Observability** — 0 of 3 done

- ⬜ OB-01 Prometheus + Grafana dashboard (B, Claude builds, you run it, week 4) ⭐
- ⬜ OB-02 OpenTelemetry tracing frontend -> backend -> LLM (A, Claude, week 4) ⭐
- ⬜ OB-03 GitOps with Argo CD or Flux (B, Claude builds, you run it, week 4) ⭐

</details>

## Change log

- 2026-09-27: DB-02: async Alembic env.py (target_metadata=Base.metadata, compare_type/compare_server_default, an advisory lock around do_run_migrations so two backend pods cannot migrate concurrently, URL from Settings() not alembic.ini). Migration 0001 creates the three Postgres enums, the complaints table with all six check constraints and both indexes, and the updated_at trigger. Found and fixed a real bug while testing offline: hand-writing constraint names as the full ck_complaints_* form in the migration produced double-prefixed names (ck_complaints_ck_complaints_text_length), because op.create_table re-applies the naming convention on top of an already-given name; switched to the same short names the ORM model uses. No Docker/Postgres here, so verified with alembic upgrade/downgrade --sql (offline mode, no DBAPI needed) plus a new regression test that diffs the migration's generated DDL against the model's own compiled DDL byte-for-byte -- confirmed it actually catches drift by deliberately breaking a column length and watching the test fail, then restored it. This stands in for alembic check, which needs a live database; a real up/down/up cycle (I21) still needs to run once Docker exists.
- 2026-09-27: DB-03: idempotent seed CLI (uv run python -m app.cli seed). SEED_NAMESPACE + uuid5(slug) gives every row a stable, deterministic id across machines and runs; insert_if_absent does ON CONFLICT (id) DO NOTHING via Postgres, so seeding twice inserts 0 rows the second time. 33 hand-written rows in app/seed/complaints.json (Urdu-English mixed text like the brief asks for, hand-written English summaries), covering every category (water 6, electricity 6, sanitation 6, roads 6, streetlights 5, other 4) and every status (open 17, in_progress 9, resolved 4, rejected 3), created_at spread over the last 14 days. The seed never calls an LLM: triaged_by is always rules, latency 0. Minimal ComplaintRepository added with just insert_if_absent (BE-02 extends it with get/list/update_status). No Docker/Postgres here, so verified two ways that need no live database: the seed algorithm itself against a fake in-memory repository (first run inserts 33, second run inserts 0, deterministic ids confirmed across two calls), and the real repository's SQL compiled against the postgresql dialect to confirm the ON CONFLICT/RETURNING clauses are correct. A live seed-twice-against-real-Postgres run is still needed once Docker exists.
- 2026-09-27: DB-01: app/db/base.py (naming convention, timestamptz type map), app/db/models.py (ComplaintORM matching plan section 9.1's table exactly -- verified by compiling every column against the real Postgres dialect), app/db/session.py (engine/sessionmaker factories). No Docker/Postgres in this sandbox, so verified via SQLAlchemy metadata introspection instead of a live database: 11 tests check column types, check-constraint names against the naming convention, both indexes, and that CreateTable DDL alone never emits CREATE TYPE (that only happens via metadata.create_all(), which app code never calls). DB-02 (Alembic) and a real Postgres round-trip are still needed before this is fully proven end to end.
- 2026-09-27: BE-01: Settings (env-only, SecretStr for passwords/API key), structlog JSON-to-stdout logging, a pure-ASGI RequestContextMiddleware (X-Request-ID echo/generate, Prometheus HTTP metrics via a dedicated CollectorRegistry, request_completed log line), the DomainError hierarchy + handlers (400/404/409/429/500, one envelope), a minimal lifecycle.py, create_app() wiring. Fixed a real bug in the plan's own literal code: computed_field(repr=False) is required or Settings.__repr__ leaks the DB password in plaintext through the assembled URL. Also swapped sqlalchemy.URL for a hand-built DSN, since app/core may not import sqlalchemy at all under our own layering rule. 3 new tests (U8, U10, I15-equivalent using capsys since structlog.testing.capture_logs bypasses the real processor chain).
- 2026-09-27: FE-09: Stats page -- CacheIndicator (HIT/MISS, fetched time, Refresh, 10s auto-refresh toggle), CSS-only CountBars for category/priority/status (no chart library), providers panel (active provider, model, cache hit rate, last-20 outcomes table with the fallback dashed-outline styling reused from ProviderTag). 3 component tests. Checked visually with Playwright, zero console errors.
- 2026-09-27: FE-07 + FE-08: Dashboard table (priority rail, category glyph, provider tag), URL-driven filters/pagination with defensive enum parsing, StatusActions with zero client-side transition table (primary buttons from allowed_transitions, Other-status menu, verbatim 409). Fixed MSW fixture dates from static future dates to dynamic offsets so relative time renders correctly; made relativeTime() robust to any date sign. 4 component tests (plan section 8.14 tests 7-10), checked visually end to end with Playwright including the 409 flow and a live URL-sync check.
- 2026-09-27: FE-05 + FE-06: full Submit page in one PR (zod validation mirroring the server, honest loading with the 8s hint, result ticket, 400 field mapping + focus, 429 countdown, network-error alert, fallback provider styling). 6 component tests (plan section 8.14 tests 1-6), checked visually with Playwright.
- 2026-09-27: FE-03: MSW handlers + typed fixtures (tests/msw/), a dev-only VITE_USE_MSW toggle (tree-shaken from prod, verified via Playwright), 5 new tests.
- 2026-09-27: Added SalmanAsadDev as Partner B in CODEOWNERS; repo invite and his own git/Claude Code setup still needed from him (see needs_you).
- 2026-09-27: FE-02: generated typed client (src/api/schema.d.ts) from backend/openapi.json; client.ts (relative baseUrl, X-Request-ID middleware), errors.ts (ApiError), enums.ts (compile-time-exact enum lists), complaints/stats/meta React Query hooks; scripts/check-contract-drift.mjs for CI; 6 new tests.
- 2026-09-27: Fixed a merge process bug: 5 stacked PRs had landed on intermediate branches instead of dev; recovered with one corrective PR (#13), no work lost, leftover branches deleted. All future PRs target dev directly.
- 2026-09-27: C0-05: stub routes for all 7 schema-visible endpoints (complaints CRUD+list, stats, providers, health/ready) plus /metrics; custom_openapi drops the automatic 422s; backend/openapi.json committed; CLI export-openapi; 7 new contract tests including a drift check against the committed file.
- 2026-09-27: C0-03: backend pyproject.toml + uv.lock (FastAPI 0.115.14, Pydantic 2.9.2, SQLAlchemy 2.0.54), ruff with the no-SQL-outside-repositories ban, mypy --strict.
- 2026-09-27: Ownership swap: A took C0-03 (to unblock the contract), B takes FE-10 (frontend test suite) to keep the commit split balanced.
- 2026-09-27: FE-04: routes, layout with nav rail (top bar under 768 px), skip link, root + per-route error boundaries, self-hosted Public Sans; 5 routing tests.
