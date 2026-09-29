# CivicPulse — status

> Generated from `docs/progress.toml` by `python scripts/update_status.py`. Edit the TOML, then regenerate. Don't edit this file by hand.
> Last updated: 2026-09-27

```text
Project progress  [█████████████░░░░░░░░░░░░░░░░░]   45%   40 of 87 core tasks done
Marks secured     [██████████░░░░░░░░░░░░░░░░░░░░]   36%   54.9 of 150 marks  (64 of 175 rubric points)
```

> ⚠️ The brief's rubric sections add up to **175** points but its header says **150** marks. Marks above are scaled ×150/175 until the instructor confirms. If the real total is 175, set `total_marks = 175` in `docs/progress.toml`.

Bonus secured: **0 of 15**. Marks are self-assessed and count a rubric line only when every task it needs is done. The final grade also applies the viva multiplier and the brief's automatic deductions.

| Partner | Core tasks done | Share of core tasks |
|---|---|---|
| Partner A (frontend, backend, data) | 27 of 38 | `███████░░░` 71% |
| Partner B (AI layer, DevOps) | 13 of 38 | `███░░░░░░░` 34% |
| Shared tasks | 0 of 11 | `░░░░░░░░░░` 0% |

## Marks by rubric section

Raw rubric points, as printed in the brief.

| Section | Secured | Out of | |
|---|---:|---:|---|
| A · Collaboration and version control | 0 | 15 | `░░░░░░░░░░` |
| B · Frontend | 15 | 18 | `████████░░` |
| C · Backend | 18 | 25 | `███████░░░` |
| D · Data layer | 10 | 12 | `████████░░` |
| E · Cache layer | 9 | 10 | `█████████░` |
| F · AI layer | 12 | 25 | `████░░░░░░` |
| G · Docker and Compose | 0 | 15 | `░░░░░░░░░░` |
| H · Kubernetes | 0 | 20 | `░░░░░░░░░░` |
| I · CI/CD | 0 | 20 | `░░░░░░░░░░` |
| J · Documentation | 0 | 15 | `░░░░░░░░░░` |
| **Total** | **64** | **175** | `███░░░░░░░` |

## Working on now

- 🔄 **C0-01** GitHub repo first: push plan + STATUS, dev branch, protection, templates, CODEOWNERS (A)
- 🔄 **AI-04** Groq provider, JSON mode, strict output validation (B)
- 🔄 **AI-08** Content-hash triage cache + measured hit rate (B)

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
- ⬜ **EV-03** Merge conflict markers / resolution / merge screenshots — you, step by step (week 2)

**Partner B (AI layer, DevOps)**

- ⬜ **DK-01** Backend multi-stage non-root Dockerfile — Claude builds, you run it (week 1)
- ⬜ **DK-02** .dockerignore per context + before/after sizes — Claude builds, you run it (week 1)
- ⬜ **DK-03** compose.yaml data tier, internal network, AOF volume — Claude builds, you run it (week 1)
- ⬜ **C0-09** Deliberate merge conflict on config.py, resolved and justified — Claude builds, you run it (week 2)

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
| 2 | 🔄 **AI-04** Groq provider, JSON mode, strict output validation | Claude builds, you run it | Create a Groq key, put it in .env only, run one live call |
| 2 | 🔄 **AI-08** Content-hash triage cache + measured hit rate | Claude builds, you run it | Run the hit-rate replay with your Groq key and paste the numbers |
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
| 2026-09-29 | **DOC-02** ADR 0001 provider interface | B |
| 2026-09-28 | **AI-11** Provider factory selected by TRIAGE_PROVIDER | B |
| 2026-09-28 | **AI-10** Outcome ring buffer + /api/meta/providers | B |
| 2026-09-28 | **CA-02** Distributed Redis rate limiter, 429 + Retry-After | A |
| 2026-09-28 | **BE-08** Architecture test, ruff banned-api, OpenAPI 400 cleanup | A |
| 2026-09-28 | **BE-07** Backend test suite (30+ tests, coverage >= 70%) | A |
| 2026-09-28 | **BE-06** SIGTERM graceful server and lifespan | A |
| 2026-09-28 | **BE-04** State machine table, PATCH status, race guard | A |
| 2026-09-28 | **BE-03** Complaint service + create/get/list routes | A |
| 2026-09-27 | **EV-01** Branch protection screenshot | B |
| 2026-09-27 | **DOC-05** ADR 0004 PII and data governance | B |
| 2026-09-27 | **CI-01** ci.yml: lint, types, contract, status, tests | B |
| 2026-09-27 | **AI-07** PII redaction (feeds ADR 0004) | B |
| 2026-09-27 | **AI-06** Prompt, injection guardrail, safety floor, injection test | B |
| 2026-09-27 | **AI-05** 10 s timeout + single jittered retry on retryable errors only | B |
| 2026-09-27 | **AI-03** TriageService skeleton + fallback + the fallback test | B |
| 2026-09-27 | **AI-02** SimulatedTriage with failure injection | B |
| 2026-09-27 | **AI-01** RuleBasedTriage + tests | B |
| 2026-09-27 | **CA-01** Stats read-through cache, X-Cache, invalidation on write | A |
| 2026-09-27 | **BE-05** /health, /ready, /metrics | A |
| 2026-09-27 | **BE-02** Repositories and unit of work | A |
| 2026-09-27 | **BE-01** Settings, JSON logging, request-id middleware, error handlers | A |
| 2026-09-27 | **DB-03** Idempotent seed CLI with 33 complaints | A |
| 2026-09-27 | **DB-02** Alembic async env with advisory lock, migration 0001 | A |
| 2026-09-27 | **DB-01** SQLAlchemy base, naming convention, ORM model | A |
| 2026-09-27 | **FE-10** Component test suite (12 tests) passing in CI | A |
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
| 2026-09-27 | **C0-04** Freeze TriageProvider / TriageResult / TriageOutcome seam | B |
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
| B5 >= 5 meaningful component tests passing in CI | 2 | ✅ | — |
| C1 All ten endpoints to contract, correct codes, field-level errors | 7 | 🔄 | FE-12 |
| C2 Four-layer separation | 4 | ✅ | — |
| C3 Explicit transition table, invalid transitions 409 | 3 | ✅ | — |
| C4 /health vs /ready, /health never touches the DB | 3 | ✅ | — |
| C5 Structured JSON logs with propagated request_id | 3 | ✅ | — |
| C6 SIGTERM drains in-flight requests | 2 | ✅ | — |
| C7 >= 14 deterministic tests, coverage >= 65% | 3 | ✅ | — |
| D1 Alembic migrations, no DDL at startup | 4 | ✅ | — |
| D2 Complete schema incl. triaged_by, ai_summary, latency, timestamptz | 3 | ✅ | — |
| D3 Two indexes, each justified by a named query | 2 | ⬜ | DB-04, DOC-07 |
| D4 Idempotent seed of >= 30 complaints | 3 | ✅ | — |
| E1 /api/stats read-through cache, 30 s TTL, X-Cache | 3 | ✅ | — |
| E2 Invalidated on write | 2 | ✅ | — |
| E3 Distributed Redis rate limiter, 429 + Retry-After | 4 | ✅ | — |
| E4 Redis AOF on a named volume, justified | 1 | ⬜ | DK-03, DOC-07 |
| F1 TriageProvider with >= 3 implementations selected by env var | 5 | 🔄 | AI-04 |
| F2 Structured output validated by Pydantic, malformed rejected safely | 5 | 🔄 | AI-04 |
| F3 Timeout, single jittered retry, fallback, triaged_by recorded | 6 | ✅ | — |
| F4 Content-hash cache with measured, reported hit rate | 3 | 🔄 | AI-08, DOC-09 |
| F5 Prompt-injection guardrail + injection test | 3 | ✅ | — |
| F6 triage_latency_ms surfaced via /api/meta/providers | 2 | ✅ | — |
| F7 PII / data-governance ADR | 1 | ✅ | — |
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
| I1 ci.yml lint, types, tests on every PR, required checks | 4 | 🔄 | CI-07 |
| I2 Compose integration smoke job | 3 | ⬜ | CI-02 |
| I3 Trivy + kubeconform in CI | 3 | ⬜ | CI-03 |
| I4 cd.yml needs-gated, GHCR images tagged by SHA | 4 | ⬜ | CI-04, CI-06 |
| I5 Ephemeral cluster deploy, rollout status, Ingress smoke test | 3 | ⬜ | CI-05 |
| I6 GitHub Secrets, scoped token, least-privilege permissions | 2 | ⬜ | CI-04, CI-05 |
| I7 Red pipeline blocking a merge, then green | 1 | ⬜ | EV-07 |
| J1 README: problem, badges, Mermaid, quickstart, API table, screenshots | 4 | ⬜ | DOC-01 |
| J2 Four ADRs | 4 | 🔄 | DOC-03, DOC-04 |
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

**Setup and contract** — 5 of 7 done

- ✅ C0-00 Implementation plan and progress tracker (A, Claude, week 1)
- 🔄 C0-01 GitHub repo first: push plan + STATUS, dev branch, protection, templates, CODEOWNERS (A, Claude builds, you run it, week 1)
- ✅ C0-02 Domain enums and Pydantic schemas (A, Claude, week 1)
- ✅ C0-03 Backend pyproject, uv lockfile, ruff, mypy (A, Claude, week 1)
- ✅ C0-04 Freeze TriageProvider / TriageResult / TriageOutcome seam (B, Claude, week 1)
- ✅ C0-05 Stub routes and committed openapi.json (A, Claude, week 1)
- ⬜ C0-09 Deliberate merge conflict on config.py, resolved and justified (Both, Claude builds, you run it, week 2)

**Frontend** — 10 of 12 done

- ✅ FE-01 Vite + React + TS strict scaffold, Tailwind, ESLint, exact versions (A, Claude, week 1)
- ✅ FE-02 Typed API client generated from OpenAPI + drift script (A, Claude, week 1)
- ✅ FE-03 MSW handlers and typed fixtures (A, Claude, week 1)
- ✅ FE-04 Router, layout, nav rail, error boundary (A, Claude, week 1)
- ✅ FE-05 Submit view: form, zod validation, honest loading, result ticket (A, Claude, week 1)
- ✅ FE-06 Submit view: 400 field mapping, 429 countdown, network errors (A, Claude, week 1)
- ✅ FE-07 Dashboard: table, URL filters, pagination (A, Claude, week 2)
- ✅ FE-08 Dashboard: server-driven transitions, verbatim 409 (A, Claude, week 2)
- ✅ FE-09 Stats view: aggregates, X-Cache indicator, providers panel (A, Claude, week 2)
- ✅ FE-10 Component test suite (12 tests) passing in CI (A, Claude, week 2)
- ⬜ FE-11 nginx runtime config template, frontend Dockerfile, .dockerignore (A, Claude builds, you run it, week 2)
- ⬜ FE-12 Switch from MSW to the real API, fix contract mismatches (A, Claude builds, you run it, week 3)

**Data layer** — 3 of 5 done

- ✅ DB-01 SQLAlchemy base, naming convention, ORM model (A, Claude, week 2)
- ✅ DB-02 Alembic async env with advisory lock, migration 0001 (A, Claude, week 2)
- ✅ DB-03 Idempotent seed CLI with 33 complaints (A, Claude, week 2)
- ⬜ DB-04 EXPLAIN evidence for both indexes at 200k rows (A, Claude, week 2)
- ⬜ DB-05 Persistence demos (Compose and Kubernetes) (A, you, step by step, week 4)

**Backend** — 8 of 8 done

- ✅ BE-01 Settings, JSON logging, request-id middleware, error handlers (A, Claude, week 2)
- ✅ BE-02 Repositories and unit of work (A, Claude, week 2)
- ✅ BE-03 Complaint service + create/get/list routes (A, Claude, week 3)
- ✅ BE-04 State machine table, PATCH status, race guard (A, Claude, week 3)
- ✅ BE-05 /health, /ready, /metrics (A, Claude, week 3)
- ✅ BE-06 SIGTERM graceful server and lifespan (A, Claude, week 3)
- ✅ BE-07 Backend test suite (30+ tests, coverage >= 70%) (A, Claude, week 3)
- ✅ BE-08 Architecture test, ruff banned-api, OpenAPI 400 cleanup (A, Claude, week 3)

**Cache** — 2 of 2 done

- ✅ CA-01 Stats read-through cache, X-Cache, invalidation on write (A, Claude, week 3)
- ✅ CA-02 Distributed Redis rate limiter, 429 + Retry-After (A, Claude, week 3)

**AI layer** — 8 of 11 done

- ✅ AI-01 RuleBasedTriage + tests (B, Claude, week 1)
- ✅ AI-02 SimulatedTriage with failure injection (B, Claude, week 1)
- ✅ AI-03 TriageService skeleton + fallback + the fallback test (B, Claude, week 1)
- 🔄 AI-04 Groq provider, JSON mode, strict output validation (B, Claude builds, you run it, week 2)
- ✅ AI-05 10 s timeout + single jittered retry on retryable errors only (B, Claude, week 2)
- ✅ AI-06 Prompt, injection guardrail, safety floor, injection test (B, Claude, week 2)
- ✅ AI-07 PII redaction (feeds ADR 0004) (B, Claude, week 2)
- 🔄 AI-08 Content-hash triage cache + measured hit rate (B, Claude builds, you run it, week 2)
- ⬜ AI-09 Ollama provider, offline profile, warm-up (B, Claude builds, you run it, week 3)
- ✅ AI-10 Outcome ring buffer + /api/meta/providers (B, Claude, week 3)
- ✅ AI-11 Provider factory selected by TRIAGE_PROVIDER (B, Claude, week 3)

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

**CI/CD** — 1 of 8 done

- ✅ CI-01 ci.yml: lint, types, contract, status, tests (B, Claude, week 1)
- ⬜ CI-02 Compose integration smoke job (MISS then HIT) (B, Claude, week 3)
- ⬜ CI-03 Image build, Trivy scan, kubeconform (B, Claude, week 3)
- ⬜ CI-04 cd.yml: needs-gated GHCR push by SHA, SBOM, least-privilege permissions (B, Claude, week 3)
- ⬜ CI-05 Ephemeral k3d deploy job, rollout status, Ingress smoke test (B, Claude builds, you run it, week 4)
- ⬜ CI-06 release.yml retagging the SHA image on v* tags (B, Claude, week 4)
- ⬜ CI-07 Required status checks wired into branch protection (B, you, step by step, week 2)
- ⬜ CI-08 Deploy by digest, Cosign sign and verify, SHA-pinned actions (B, Claude, week 4) ⭐

**Documentation** — 2 of 10 done

- ⬜ DOC-01 README with badges, Mermaid, quickstart, API table, screenshots (Both, Claude builds, you run it, week 4)
- ✅ DOC-02 ADR 0001 provider interface (B, Claude, week 4)
- ⬜ DOC-03 ADR 0002 frontend runtime config (A, Claude, week 4)
- ⬜ DOC-04 ADR 0003 deploy by SHA (B, Claude, week 4)
- ✅ DOC-05 ADR 0004 PII and data governance (B, Claude, week 2)
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

- 2026-09-29: DOC-02: docs/adr/0001-provider-interface.md, justifying the two design decisions behind app/providers/triage/base.py::TriageProvider -- async over the brief's own printed sync signature (every real provider is I/O-bound, and TriageService needs one generic await path under asyncio.timeout(), not a per-provider sync/async branch), and Protocol over an ABC (no shared behaviour to inherit, and RuleBasedTriage's dual role as both a provider and TriageService's fallback would make an ABC's inheritance mean something it doesn't). Verified two claims against the actual code before writing them down rather than assuming from the plan's prose: runtime_checkable is genuinely decorative today (grepped for isinstance(x, TriageProvider) -- zero hits), and triage_sync() has exactly two real callers (TriageService's fallback path and SimulatedTriage), not three as first drafted -- the safety floor turned out to check HIGH_RISK keywords directly rather than calling into RuleBasedTriage at all.
- 2026-09-28: AI-08 (cache + hit-rate mechanism done; the duplicate-replay measurement is the pending human step): app/providers/triage/cache.py::TriageResultCache, wired into factory.py's build_triage_service so TRIAGE_PROVIDER=llm/ollama now actually get a Redis-backed cache instead of the permanent-miss NullTriageCache. Key excludes location on purpose (plan section 11.7: nine neighbours reporting the same burst main should cost one inference) and includes provider/model/PROMPT_VERSION so switching any of them can never serve a stale classification. Hit/miss counters (triage:stats:hits/misses) live in Redis, not memory, for the same distributed-state reason AI-10's OutcomeLog does -- proven across two TriageResultCache instances sharing one fakeredis, the same pattern test_outcomes.py's A16 already used. Added TriageCache.hit_rate() to the Protocol (NullTriageCache returns None) and TriageService.cache_hit_rate(), so MetaService now reports the real measured rate through /api/meta/providers instead of the AI-08-shaped None placeholder -- the one route change in this task, and it only reads through TriageService's existing public surface, per that module's own layering rule. 12 new tests (test_triage_cache.py: hit/miss/key-shape/TTL/hit-rate; plus 3 more in test_triage_service.py and 2 updated in test_meta_service.py). 271 tests passing, 91.96% coverage (triage_service.py itself now 100%); ruff/format/mypy clean; confirmed no OpenAPI drift (no route shape changed, only its cache_hit_rate value stopped being hardcoded). What is NOT done: the plan's own AI-08 acceptance needs a measured hit rate from replaying load/duplicates.jsonl against a real Groq key (docs/TRIAGE.md, DOC-09) -- that dataset and that replay script do not exist yet either, and both need a real key this sandbox doesn't have. Left status in_progress rather than done.
- 2026-09-28: AI-04 (code + tests only, human step still pending): GroqTriage (app/providers/triage/llm.py) -- an AsyncOpenAI client pointed at Groq's OpenAI-compatible endpoint, max_retries=0 so TriageService (AI-05) owns the single retry, JSON mode, temperature=0. Wired into factory.py: TRIAGE_PROVIDER=llm now selects it when groq_api_key is set, and still degrades to rules with an ERROR log (not a crash) when it is not, matching the plan's own build_primary snippet exactly. redact() runs on the complaint text before it is sent, and location/reporter_contact are never included in the request at all -- both proven by inspecting the actual call kwargs sent to a mocked client, the same no-live-call testing pattern AI-01/02/05/06 already used (no respx dependency needed for this). 9 new tests in test_llm_triage.py (A2: malformed JSON and an invalid enum value both raise MalformedOutput rather than being accepted best-effort; A15: no location/contact, PII redacted; plus the max_retries=0 / JSON-mode / model wiring itself) and 2 updated tests in test_factory.py. 260 tests passing (1 deselected), 91.75% coverage; ruff/format/mypy clean -- mypy needed one explicit cast, since build_messages()'s list[dict[str, str]] does not structurally match the SDK's ChatCompletionMessageParam TypedDict union. What is NOT done here, per the plan's own AI-04 acceptance ('manual call succeeds'): no real Groq key exists in this sandbox, so the one live call against the actual API has not been made. Left status in_progress rather than done until that human step happens.
- 2026-09-28: BE-07 closed out: the 249-test / 91.6%-coverage suite from the batched run above already exceeds the plan's 30+/>=70% acceptance bar, so the remaining work was tightening the enforced floor to match rather than adding tests for their own sake. Raised coverage.report.fail_under from 65 to 70 in backend/pyproject.toml, and the matching --cov-fail-under flag in ci.yml's test-backend job from 65 to 70, so both local and CI runs honestly enforce the plan's stated target instead of a looser placeholder. Reran the exact CI command afterward: 249 passed, 1 deselected, 91.59% coverage, comfortably above the new floor. The one remaining gap -- the integration-marked create-complaint test needing real Postgres/Redis -- is out of scope here: ci.yml's own comment assigns that to CI-02's Compose integration job (owner B), not to BE-07's testcontainers wiring, so conftest.py is left as-is.
- 2026-09-28: Timeline compressed to "finish tonight": dropped the week-based sequencing and batched seven tightly-coupled backend/AI tasks in one run instead of one task per PR -- AI-11 (provider factory), AI-10 (Redis outcome log + real /api/meta/providers), BE-03 (real ComplaintService, replacing the C0-05 stub routes), BE-04 (state machine + PATCH + optimistic-concurrency race guard), BE-06 (GracefulServer: SIGTERM flips readiness before uvicorn drains, not after), CA-02 (Redis fixed-window rate limiter, atomic INCR+EXPIRE via Lua), BE-08 (AST-based architecture test; OpenAPI 400 cleanup was already done by C0-05). Testing all seven together surfaced issues a one-task-at-a-time pass would have hit piecemeal anyway, worth listing because they explain real code choices: (1) the CA-02 tests need fakeredis's real Lua backend (`lupa`), missing from both this sandbox and the dev dependency group -- added it and regenerated uv.lock (uv itself had to be installed fresh here to do that). (2) mypy under the *actually pinned* SQLAlchemy 2.0.54 (this sandbox had drifted to 2.1.1 again) flagged a real bug in outcomes.py: redis-py 5.3.1's lrange() stub returns a union type that fails a bare `await`; fixed with an explicit Awaitable cast. (3) Two pre-existing observability tests (U8, I15) built their TestClient without entering the app lifespan, which the C0-05 stub routes never needed but the new real routes do -- fixed by entering it (U8) or faking the dependency directly (I15, since /health/ready/metrics are deliberately excluded from request-completed logging and can't stand in). (4) test_contract.py's create-complaint test now genuinely needs a live Postgres now that BE-03 wired the real service, and conftest.py has no testcontainers fixtures yet (that's BE-07/CI-02's job) -- marked it `integration` and excluded that marker in ci.yml's test-backend job rather than leave a test CI cannot actually pass. 249 tests passing (1 deselected), 91.6% coverage; ruff/format/mypy clean under the CI-accurate uv-managed venv; no OpenAPI drift.
- 2026-09-27: AI-07 + DOC-05: PII redaction (app/providers/triage/redaction.py::redact(), the plan's four patterns verbatim -- PK mobile, CNIC, email, house/plot address) and ADR 0004. Verified against the real seed data, not just hand-picked examples: three rows in app/seed/complaints.json actually contain a house number in text or location, and redact() catches all three. The ADR is written to distinguish what already exists (redact() itself, parsing.py's include_input=False) from what AI-04's not-yet-built GroqTriage is required to do (call redact(), never send reporter_contact/location) -- test A15 verifies that requirement once AI-04 lands. 14 tests (A14 parametrized over every pattern, plus that ordinary numbers and addresses are left alone).
- 2026-09-27: AI-06: prompt module (app/providers/triage/prompt.py, PROMPT_VERSION + SYSTEM + build_messages with delimiter neutralization) and the safety floor (_apply_safety_floor in triage_service.py): a HIGH_RISK keyword in the complaint text always forces priority=high, regardless of what the primary returned, applied on both a fresh primary success and a cache hit (proven with a cache seeded directly, bypassing write-time application, to show the read-time floor also catches it). A11 (the brief's injection test) needed no new mechanism at all: an LLM asked to return category='hacked' produces an invalid enum value, which is already MalformedOutput under AI-02/AI-03's existing validation, so it already falls back to rules -- the injection test is really proving the fallback path, not a new guardrail. 9 tests: A11, A12 (delimiter neutralization, both directions), A13 (safety floor overriding a valid-but-wrong low priority), plus that the floor leaves a correct high priority and ordinary text alone.
- 2026-09-27: FE-10 revisited: the ownership-swap plan (above) had B write the frontend test suite, but in practice A's own FE-05/06/07/08/09 PRs already wrote all 12 tests plan section 8.14 names for this task (6 in SubmitPage, 4 in Dashboard, the X-Cache test in Stats, and a crash-and-recover test already in routing.test.tsx covering the same behavior section 8.14 names ErrorBoundary.test.tsx for) -- 29 tests total, confirmed green in CI. Rather than write a redundant test file just to have a B-owned commit against this task ID, marking it done under owner A, since that's who actually holds the commits: task-ID ownership is bookkeeping, but A2/A4 (commit-split >= 35% each) is graded on real commit authorship, and this would have misrepresented it.
- 2026-09-27: AI-05: TriageService timeout and retry policy (_call_primary() under asyncio.timeout(10s), exactly one retry for the RETRYABLE set only; sleep/rng injectable for deterministic tests). OllamaServerError moved to its own app/providers/triage/errors.py since RETRYABLE needs it ahead of AI-09. 14 tests (A3-A7 plus one for the successful-retry path); added S311 to the tests ruff ignore list (seeded random.Random() for deterministic timing, the same kind of case S106 already covers).
- 2026-09-27: CI-01: .github/workflows/ci.yml with the five checks that don't need Docker or Kubernetes yet -- lint-and-type, contract, status, test-backend, test-frontend (build/scan/manifests/integration wait for CI-02/CI-03 once DK-01..03 exist). Before shipping it, ran every job's exact commands locally to make sure a clean PR is actually green, not just plausible, and that surfaced two more pre-existing issues: a real mypy error in complaint_repository.py (get_status_stmt was typed Select[Any], so get_status() silently returned Any instead of Status | None -- fixed by typing it Select[Status]), and a Node-version trap in the frontend test job (this sandbox's Node 24 fails 2 tests with an AbortSignal cross-realm error from MSW's interceptor against Node's undici; confirmed clean on a portable Node 22.20.0, which is what ci.yml actually pins, so left the test code untouched). Full local dry run once both were fixed: backend ruff/format/mypy clean, 102 tests passing at 87.9% coverage; frontend lint/typecheck clean, 29 tests passing, build succeeds; openapi.json and schema.d.ts both drift-free; STATUS.md in sync.
- 2026-09-27: AI-03: TriageService skeleton + fallback (app/services/triage_service.py). Writing the fallback test surfaced a real bug in the plan's own literal code: its triage() snippet caches the primary's result unconditionally on success, contradicting its own stated design ("no cache is used [for rules], since rules are cheaper than Redis") -- a rules-as-primary run would still round-trip Redis on every request. Guarded the cache write with the same `primary.name != "rules"` check already used on the read side. 8 tests: A1 (AlwaysRaisesProvider -> rules:fallback), successful/cached/rules-primary paths, and that CancelledError propagates instead of being swallowed (needed for BE-06's graceful shutdown later).
- 2026-09-27: AI-02: SimulatedTriage (app/providers/triage/simulated.py) and the shared parse_triage_output/MalformedOutput (app/providers/triage/parsing.py, which AI-04's GroqTriage will reuse as-is). All four failure modes (raise, timeout, malformed, rate_limited) produce the exact exception types TriageService's retry policy (AI-05) will need to distinguish, including a real openai.RateLimitError built from a fake httpx.Response rather than a hand-rolled stand-in. 7 tests, including a monkeypatched socket.socket that asserts a normal call opens no socket at all ("no network, ever").
- 2026-09-27: AI-01: RuleBasedTriage (app/providers/triage/rules.py), matching the plan's keyword table verbatim -- 93.9% category accuracy (31/33) against the seed set, well over the required 70%, so no tuning was needed. Shared normalize()/first_sentence() helpers split into app/providers/triage/text.py so AI-08's cache can reuse the same normalize() later. 6 tests: the accuracy threshold, determinism, high-risk and low-hint priority rules, the other-category fallback, and totality against 6 edge-case strings (max length, punctuation-only, non-Latin script, mixed case, combining-character normalization).
- 2026-09-27: C0-04: froze the triage seam -- app/providers/triage/base.py (TriageResult, the TriageProvider Protocol) and app/services/triage_service.py (TriageOutcome, TriageService.triage()/recent_outcomes()/active_provider). TriageCache and OutcomeSink are Protocols with Null* default implementations, so the skeleton works today without AI-08's Redis cache or AI-10's Redis outcome log -- both will satisfy the same Protocols later without touching TriageService's constructor or callers. tests/fakes.py::StubTriageService added per the plan so ComplaintService (BE-03) can be coded against the seam before AI-04 lands.
- 2026-09-27: Partner B (Salman) starts picking up Partner B's backlog directly, since Ibrahim is stepping back from active contribution for a while. Before starting on the prescribed AI-layer work, fixed a real bug Salman hit running the app locally: every page other than Submit crashed with the app's own "This page stopped working" boundary as soon as the backend was unreachable (e.g. no Docker running). Root cause: stats.ts/meta.ts/complaints.ts treated the parsed error body's truthiness, not response.ok, as the signal that a request had failed; the dev proxy answers an unreachable backend with a 500 that has an empty, non-JSON body, which parses to a falsy `error`, so the check silently passed and StatsPage crashed reading `.stats.total` off a `data` object that looked loaded but was not. Fixed by checking `error || !response.ok` everywhere (keeping the `error` check too, since openapi-fetch's TS types only narrow `data` to defined off that check, not off response.ok -- dropping it re-broke typecheck across four files). Committed separately on fix/stats-page-crash-on-api-failure pending push.
