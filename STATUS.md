# CivicPulse — status

> Generated from `docs/progress.toml` by `python scripts/update_status.py`. Edit the TOML, then regenerate. Don't edit this file by hand.
> Last updated: 2026-09-27

```text
Project progress  [████████████████░░░░░░░░░░░░░░]   56%   49 of 87 core tasks done
Marks secured     [██████████████░░░░░░░░░░░░░░░░]   48%   72.9 of 150 marks  (85 of 175 rubric points)
```

> ⚠️ The brief's rubric sections add up to **175** points but its header says **150** marks. Marks above are scaled ×150/175 until the instructor confirms. If the real total is 175, set `total_marks = 175` in `docs/progress.toml`.

Bonus secured: **0 of 15**. Marks are self-assessed and count a rubric line only when every task it needs is done. The final grade also applies the viva multiplier and the brief's automatic deductions.

| Partner | Core tasks done | Share of core tasks |
|---|---|---|
| Partner A (frontend, backend, data) | 29 of 38 | `███████░░░` 76% |
| Partner B (AI layer, DevOps) | 19 of 38 | `█████░░░░░` 50% |
| Shared tasks | 1 of 11 | `░░░░░░░░░░` 9% |

## Marks by rubric section

Raw rubric points, as printed in the brief.

| Section | Secured | Out of | |
|---|---:|---:|---|
| A · Collaboration and version control | 0 | 15 | `░░░░░░░░░░` |
| B · Frontend | 18 | 18 | `██████████` |
| C · Backend | 25 | 25 | `██████████` |
| D · Data layer | 10 | 12 | `████████░░` |
| E · Cache layer | 9 | 10 | `█████████░` |
| F · AI layer | 12 | 25 | `████░░░░░░` |
| G · Docker and Compose | 11 | 15 | `███████░░░` |
| H · Kubernetes | 0 | 20 | `░░░░░░░░░░` |
| I · CI/CD | 0 | 20 | `░░░░░░░░░░` |
| J · Documentation | 0 | 15 | `░░░░░░░░░░` |
| **Total** | **85** | **175** | `████░░░░░░` |

## Working on now

- 🔄 **C0-01** GitHub repo first: push plan + STATUS, dev branch, protection, templates, CODEOWNERS (A)
- 🔄 **AI-04** Groq provider, JSON mode, strict output validation (B)
- 🔄 **AI-08** Content-hash triage cache + measured hit rate (B)
- 🔄 **AI-09** Ollama provider, offline profile, warm-up (B)
- 🔄 **DOC-08** AI-USAGE.md (Both)

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
- ⬜ **DB-04** EXPLAIN evidence for both indexes at 200k rows — Claude (week 2)
- ⬜ **EV-03** Merge conflict markers / resolution / merge screenshots — you, step by step (week 2)
- ⬜ **EV-02** 5+ merged PRs linked to Issues with substantive reviews — your partner (week 3)

**Partner B (AI layer, DevOps)**

- ⬜ **C0-09** Deliberate merge conflict on config.py, resolved and justified — Claude builds, you run it (week 2)
- ⬜ **CI-07** Required status checks wired into branch protection — you, step by step (week 2)
- ⬜ **EV-03** Merge conflict markers / resolution / merge screenshots — you, step by step (week 2)
- ⬜ **K8-01** k3d cluster, namespace, ConfigMap, placeholder Secret, Postgres StatefulSet, Redis — Claude builds, you run it (week 3)

## Hands-on work for you and your partner

Claude does every task marked "Claude". These are the ones that need a person. Claude gives step-by-step instructions for each one when it comes up.

| Week | Task | Who | What you do |
|---:|---|---|---|
| 1 | 🔄 **C0-01** GitHub repo first: push plan + STATUS, dev branch, protection, templates, CODEOWNERS | Claude builds, you run it | Create the repo (or connect GitHub), add your partner, turn on branch protection |
| 2 | ⬜ **C0-09** Deliberate merge conflict on config.py, resolved and justified | Claude builds, you run it | You and your partner each commit one side from your own accounts, then screenshot |
| 2 | 🔄 **AI-04** Groq provider, JSON mode, strict output validation | Claude builds, you run it | Create a Groq key, put it in .env only, run one live call |
| 2 | 🔄 **AI-08** Content-hash triage cache + measured hit rate | Claude builds, you run it | Run the hit-rate replay with your Groq key and paste the numbers |
| 2 | ⬜ **CI-07** Required status checks wired into branch protection | you, step by step | All of it, following Claude's steps |
| 2 | ⬜ **EV-03** Merge conflict markers / resolution / merge screenshots | you, step by step | All of it, following Claude's steps |
| 3 | 🔄 **AI-09** Ollama provider, offline profile, warm-up | Claude builds, you run it | Install Ollama's model via make offline and paste the latency numbers |
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
| 4 | 🔄 **DOC-08** AI-USAGE.md | Claude builds, you run it | Confirm the AI-USAGE account of what Claude wrote is accurate; Salman fills in his own AI-tool-usage row |
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
| 2026-09-29 | **DK-07** Image size report (build stage vs final) | Both |
| 2026-09-29 | **DK-06** Offline profile with ollama_models volume | B |
| 2026-09-29 | **DK-05** compose.prod.yaml (image by tag, no build, no DB/cache ports) | B |
| 2026-09-29 | **DK-04** migrate + seed services, healthchecks, make up | B |
| 2026-09-29 | **DK-03** compose.yaml data tier, internal network, AOF volume | B |
| 2026-09-29 | **DK-02** .dockerignore per context + before/after sizes | B |
| 2026-09-29 | **DK-01** Backend multi-stage non-root Dockerfile | B |
| 2026-09-29 | **FE-12** Switch from MSW to the real API, fix contract mismatches | A |
| 2026-09-29 | **FE-11** nginx runtime config template, frontend Dockerfile, .dockerignore | A |
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
| B4 Runtime configuration, one image for every environment | 3 | ✅ | — |
| B5 >= 5 meaningful component tests passing in CI | 2 | ✅ | — |
| C1 All ten endpoints to contract, correct codes, field-level errors | 7 | ✅ | — |
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
| E4 Redis AOF on a named volume, justified | 1 | 🔄 | DOC-07 |
| F1 TriageProvider with >= 3 implementations selected by env var | 5 | 🔄 | AI-04 |
| F2 Structured output validated by Pydantic, malformed rejected safely | 5 | 🔄 | AI-04 |
| F3 Timeout, single jittered retry, fallback, triaged_by recorded | 6 | ✅ | — |
| F4 Content-hash cache with measured, reported hit rate | 3 | 🔄 | AI-08, DOC-09 |
| F5 Prompt-injection guardrail + injection test | 3 | ✅ | — |
| F6 triage_latency_ms surfaced via /api/meta/providers | 2 | ✅ | — |
| F7 PII / data-governance ADR | 1 | ✅ | — |
| G1 Both images multi-stage, pinned, non-root, exec CMD, cache-correct | 4 | ✅ | — |
| G2 .dockerignore per context with before/after sizes | 2 | ✅ | — |
| G3 Two networks, internal: true, frontend provably can't reach DB | 4 | 🔄 | EV-06 |
| G4 Three named volumes justified, dev bind mount only in dev | 2 | ✅ | — |
| G5 Healthchecks + depends_on service_healthy | 2 | ✅ | — |
| G6 compose.prod.yaml: image tag, no build, no DB/cache port | 1 | ✅ | — |
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

**Frontend** — 12 of 12 done

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
- ✅ FE-11 nginx runtime config template, frontend Dockerfile, .dockerignore (A, Claude builds, you run it, week 2)
- ✅ FE-12 Switch from MSW to the real API, fix contract mismatches (A, Claude builds, you run it, week 3)

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
- 🔄 AI-09 Ollama provider, offline profile, warm-up (B, Claude builds, you run it, week 3)
- ✅ AI-10 Outcome ring buffer + /api/meta/providers (B, Claude, week 3)
- ✅ AI-11 Provider factory selected by TRIAGE_PROVIDER (B, Claude, week 3)

**Docker and Compose** — 7 of 7 done

- ✅ DK-01 Backend multi-stage non-root Dockerfile (B, Claude builds, you run it, week 1)
- ✅ DK-02 .dockerignore per context + before/after sizes (B, Claude builds, you run it, week 1)
- ✅ DK-03 compose.yaml data tier, internal network, AOF volume (B, Claude builds, you run it, week 1)
- ✅ DK-04 migrate + seed services, healthchecks, make up (B, Claude builds, you run it, week 2)
- ✅ DK-05 compose.prod.yaml (image by tag, no build, no DB/cache ports) (B, Claude builds, you run it, week 3)
- ✅ DK-06 Offline profile with ollama_models volume (B, Claude builds, you run it, week 3)
- ✅ DK-07 Image size report (build stage vs final) (Both, Claude builds, you run it, week 3)

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
- 🔄 DOC-08 AI-USAGE.md (Both, Claude builds, you run it, week 4)
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

- 2026-09-29: DOC-08: docs/AI-USAGE.md, written from this session's own real record (docs/progress.toml's [[log]] entries and actual git history) rather than a generic AI-usage template. Names the tool (Claude Code / Claude Sonnet 5) and covers, with specific file/task citations: what it was used for, four verbatim representative prompts from this session, and eight concrete rejected-or-corrected cases spanning a bug in the plan's own reference code (AI-03), a real Alembic naming bug (DB-02), two real mypy --strict catches (CI-01, AI-10), a rejected sync interface from the brief itself (DOC-02/ADR 0001), a factual error in Claude's own first ADR 0001 draft caught and fixed before commit, an avoided-not-corrected redundant test file (FE-10), and a too-loose coverage floor (BE-07). Left status in_progress: the task's own human field asks you to confirm the account is accurate, and asks Salman to add his own AI-tool-usage row rather than have it written on his behalf.
- 2026-09-29: DK-05 + DK-06 + DK-07, closing out the Docker/Compose backlog. DK-05: compose.prod.yaml, an override applied via `docker compose -f compose.yaml -f compose.prod.yaml up` -- swaps backend/frontend/migrate/seed's `build:` for pre-built `image: ghcr.io/.../civicpulse-*:${IMAGE_TAG}` references using the Compose Specification's `!reset null` merge tag (plain key overriding is not enough: if `build:` survived the merge, `docker compose up` would still build locally instead of pulling the image CI-04's pipeline already tested; confirmed via `docker compose -f compose.yaml -f compose.prod.yaml config` that no `build:` key and no Postgres/Redis port survive the merge). DK-06: an `ollama` service under compose's `profiles: ["offline"]` (not started by plain `make up`), on a named `ollama_models` volume so a pulled model survives a restart, healthchecked via `ollama list`; root Makefile gained `make offline`. Verified for real, not just config: brought the profile up, watched it go `healthy`, then stopped it -- did not run the actual model pull (`ollama pull llama3.2:1b`), since that is explicitly AI-09's own pending human step, not this task's. DK-07: docs/evidence/06-image-sizes.txt and 05-build-context.txt, both from real measurements, not assumptions -- backend 276MB (vs a throwaway 1.9GB naive single-stage build), frontend 74.3MB (nginxinc/nginx-unprivileged:1.27-alpine base is itself 38.7MB per `docker history`; the plan's own internal target for this file was under 60MB, reported honestly as the real 74.3MB instead). One methodology problem surfaced and worked around while gathering build-context evidence: a live before/after `docker build --no-cache` pair (the plan's own suggested script) reported an implausible ~13kB context even with .dockerignore renamed out of the way, because BuildKit's context-transfer session dedups by content hash across builds on the same builder instance regardless of --no-cache (which only disables instruction/layer caching, not that) -- switched to `du -sh` for the honest "before" number (backend 436MB including both local venvs; frontend 217MB, almost entirely node_modules) while keeping the real, live BuildKit-reported "after" numbers.
- 2026-09-29: FE-11 + DK-04: frontend/Dockerfile (multi-stage: node:22.20.0-alpine builds the Vite bundle, nginxinc/nginx-unprivileged:1.27-alpine serves it -- non-root by default, 74.3MB). Runtime config is a single env var, not a JS config blob: the client already used a relative baseUrl (src/api/client.ts, plan section 8.1's own ban on VITE_API_*), so the only per-environment knob left is where nginx proxies /api/ to -- frontend/nginx/default.conf.template's ${BACKEND_HOST}/${BACKEND_PORT} are envsubst'd by nginx's own entrypoint scripts at container start, so the identical built image works in compose (BACKEND_HOST=backend) and later in Kubernetes (a Service DNS name) without a rebuild (rubric B4). One real bug caught building it: frontend/.dockerignore's first draft excluded tests/ wholesale, which broke `tsc -b` -- main.tsx dynamically imports tests/msw/browser (dead-code-eliminated from the actual bundle by Vite, but still resolved at compile time), so only node_modules/dist/coverage/.vite are excluded, not tests/ itself. compose.yaml gained the app tier: migrate and seed as one-shot services (restart: "no", gated on service_healthy / service_completed_successfully so seed can never race migrate), backend healthchecked via its own venv's python hitting /health (no curl/wget in python:3.12-slim), frontend on a second, non-internal `app` network -- attached to the backend, never to `data`. Root Makefile (`make up` == `docker compose up -d --build`). Verified for real: brought the whole stack up from cold with `docker compose up -d --build`, confirmed the dependency chain actually gated correctly (migrate ran and exited 0 before seed started, seed exited 0 before backend's healthcheck could pass, frontend didn't start until backend was healthy), hit the frontend's published port and got a real 200 with real seeded data through the nginx proxy (`GET :8080/api/stats` -> 33 complaints), and confirmed from inside the frontend container itself that `database` doesn't even resolve -- G3's network isolation holds with the full app tier wired in, not just the bare data tier from DK-03.
- 2026-09-29: AI-09 (provider code + tests done; installing a model and measuring latency is the pending human/DK-06 step): app/providers/triage/ollama.py::OllamaTriage, matching the plan's exact design -- POST /api/chat with stream=false and format=TriageResult.model_json_schema() so Ollama's structured-output mode constrains decoding, options.temperature=0. Unlike GroqTriage it applies no PII redaction, since nothing leaves the machine running Ollama; also unlike GroqTriage it does not own its http client -- OllamaTriage takes a shared httpx.AsyncClient, so app/core/lifecycle.py now opens one real client at startup (app.state.http) and closes it at shutdown alongside Redis and the DB engine, and factory.py threads it through build_triage_service/build_primary. A 5xx maps to the already-retryable OllamaServerError; a 4xx still raises (via raise_for_status()) but as a plain httpx.HTTPStatusError, deliberately not retried, the same as GroqTriage's 400/401/403. 13 new/updated tests (8 for OllamaTriage: valid parse, request shape, no-redaction, 5xx vs 4xx handled differently, malformed/invalid-enum both fall back safely; 5 updated in test_factory.py for the new http-threading signature, plus a new ollama selection test). 280 tests passing, 92.26% coverage; ruff/format/mypy clean; confirmed no OpenAPI drift. What is NOT done: the plan's own AI-09 acceptance needs an actual model installed (`make offline`, DK-06, owner B) and measured latency p50/p95 against the seed set for docs/TRIAGE.md -- no Ollama binary or Docker in this sandbox to do either. Left status in_progress rather than done.
- 2026-09-29: FE-12: confirmed the two halves of "switch from MSW to the real API" that were already true (MSW is opt-in behind VITE_USE_MSW and dead-code-eliminated from the production build since FE-03; the typed client already calls the real endpoints, so there was never a literal "switch" to perform) and found the one real contract mismatch: app/pages/ComplaintDetailPage.tsx was still FE-02's original placeholder ("Placeholder until the API client exists"), rendering only the raw id, even though the real GET /api/complaints/{id} route (BE-03) and its typed useComplaint(id) hook had existed for a while unused. Wired it up per plan section 8.11: full text, all fields, StatusActions, both timestamps, and a 404/400 rendered the same way -- the server's message verbatim plus a link back to the dashboard, matching the app's existing rule that the frontend never rewrites what the backend said. 2 new tests. Verified without a live backend (no Postgres in this sandbox): npm run gen:api + check:contract show zero drift between the committed openapi.json and schema.d.ts, and the full suite (31 tests), typecheck, lint, and build are all clean.
- 2026-09-29: DOC-02: docs/adr/0001-provider-interface.md, justifying the two design decisions behind app/providers/triage/base.py::TriageProvider -- async over the brief's own printed sync signature (every real provider is I/O-bound, and TriageService needs one generic await path under asyncio.timeout(), not a per-provider sync/async branch), and Protocol over an ABC (no shared behaviour to inherit, and RuleBasedTriage's dual role as both a provider and TriageService's fallback would make an ABC's inheritance mean something it doesn't). Verified two claims against the actual code before writing them down rather than assuming from the plan's prose: runtime_checkable is genuinely decorative today (grepped for isinstance(x, TriageProvider) -- zero hits), and triage_sync() has exactly two real callers (TriageService's fallback path and SimulatedTriage), not three as first drafted -- the safety floor turned out to check HIGH_RISK keywords directly rather than calling into RuleBasedTriage at all.
- 2026-09-28: AI-08 (cache + hit-rate mechanism done; the duplicate-replay measurement is the pending human step): app/providers/triage/cache.py::TriageResultCache, wired into factory.py's build_triage_service so TRIAGE_PROVIDER=llm/ollama now actually get a Redis-backed cache instead of the permanent-miss NullTriageCache. Key excludes location on purpose (plan section 11.7: nine neighbours reporting the same burst main should cost one inference) and includes provider/model/PROMPT_VERSION so switching any of them can never serve a stale classification. Hit/miss counters (triage:stats:hits/misses) live in Redis, not memory, for the same distributed-state reason AI-10's OutcomeLog does -- proven across two TriageResultCache instances sharing one fakeredis, the same pattern test_outcomes.py's A16 already used. Added TriageCache.hit_rate() to the Protocol (NullTriageCache returns None) and TriageService.cache_hit_rate(), so MetaService now reports the real measured rate through /api/meta/providers instead of the AI-08-shaped None placeholder -- the one route change in this task, and it only reads through TriageService's existing public surface, per that module's own layering rule. 12 new tests (test_triage_cache.py: hit/miss/key-shape/TTL/hit-rate; plus 3 more in test_triage_service.py and 2 updated in test_meta_service.py). 271 tests passing, 91.96% coverage (triage_service.py itself now 100%); ruff/format/mypy clean; confirmed no OpenAPI drift (no route shape changed, only its cache_hit_rate value stopped being hardcoded). What is NOT done: the plan's own AI-08 acceptance needs a measured hit rate from replaying load/duplicates.jsonl against a real Groq key (docs/TRIAGE.md, DOC-09) -- that dataset and that replay script do not exist yet either, and both need a real key this sandbox doesn't have. Left status in_progress rather than done.
- 2026-09-29: DK-02 (backend half): .dockerignore excludes both local venvs, tests/, caches and .env* from the build context. Measured, not assumed: a naive single-stage Dockerfile (python:3.12 full, one RUN uv sync with build tools left in) produced a 1.9GB image; the multi-stage slim build above produces 276MB -- an 85% reduction. The naive Dockerfile and its image were throwaway, used only to get this number, and were deleted afterward. Left in_progress: DK-02's other context (frontend) is FE-11's job (nginx template + frontend Dockerfile), not yet done.
- 2026-09-29: DK-01 + DK-03: backend/Dockerfile (multi-stage: uv==0.5.11 in a python:3.12-slim builder installing frozen deps with --no-install-project before app code is copied in, so editing app code never invalidates the dependency layer; non-root `app` user in the runtime stage; exec-form CMD ["python", "-m", "app.server"] so SIGTERM reaches BE-06's GracefulServer directly, not a shell). compose.yaml adds the data tier only (DK-04 wires the app services): `database`/`cache` service names match Settings' own defaults exactly, so the backend needs zero host overrides once attached; an `internal: true` network with no published ports; Redis with --appendonly yes on a named volume (redis-data) since the rate limiter's window counters and the outcome ring buffer are live state a bare restart shouldn't reset; both services have real healthchecks (pg_isready; redis-cli -a <password> ping, using compose's own parse-time ${VAR} substitution after an escaping bug -- $${REDIS_PASSWORD} -- made the first attempt fail with WRONGPASS since nothing had put the variable into the container's own runtime env). .env.example added at the repo root (POSTGRES_PASSWORD, REDIS_PASSWORD); .gitignore already covered .env. Verified for real, not just `compose config`: built the image, brought the data tier up, ran `alembic upgrade head` and the seed CLI from inside the built image against it (both succeeded, confirming the DB-02 fix above holds under Docker too, not just the manual container), ran the backend image itself joined to the network and hit /health, /ready (postgres+redis both "ok") and /api/stats over a real request, and confirmed a container NOT on the `data` network cannot resolve `database` at all -- proving the network isolation rubric (G3) actually holds, not just that the YAML says internal: true.
- 2026-09-29: Root-caused and fixed a real bug in DB-02's own Alembic env.py while getting the stack running locally for the first time with Docker Desktop finally stable: do_run_migrations's advisory-lock SELECT (`pg_advisory_lock`) autobegins a real SQLAlchemy transaction before context.begin_transaction() runs, so alembic nests the actual migration inside a SAVEPOINT instead of a top-level transaction; run_async_migrations then used engine.connect() (closes without committing) instead of engine.begin() (commits on clean exit), so every `alembic upgrade head` printed a normal success line and genuinely executed the DDL, then silently rolled the whole thing back the instant the connection closed. Diagnosed by ruling out the more obvious suspects first (IPv6/wslrelay port collision, a second Postgres on the same port, a restarted container with a fresh volume -- all checked and cleared) before reading env.py itself. One-line fix: connectable.begin() instead of connectable.connect(). Confirmed fixed against both the manually-run postgres:16-alpine container and, later the same day, the new compose-managed one -- `\dt` now shows complaints + alembic_version after every run, and the seed CLI inserted all 33 rows.
- 2026-09-28: AI-04 (code + tests only, human step still pending): GroqTriage (app/providers/triage/llm.py) -- an AsyncOpenAI client pointed at Groq's OpenAI-compatible endpoint, max_retries=0 so TriageService (AI-05) owns the single retry, JSON mode, temperature=0. Wired into factory.py: TRIAGE_PROVIDER=llm now selects it when groq_api_key is set, and still degrades to rules with an ERROR log (not a crash) when it is not, matching the plan's own build_primary snippet exactly. redact() runs on the complaint text before it is sent, and location/reporter_contact are never included in the request at all -- both proven by inspecting the actual call kwargs sent to a mocked client, the same no-live-call testing pattern AI-01/02/05/06 already used (no respx dependency needed for this). 9 new tests in test_llm_triage.py (A2: malformed JSON and an invalid enum value both raise MalformedOutput rather than being accepted best-effort; A15: no location/contact, PII redacted; plus the max_retries=0 / JSON-mode / model wiring itself) and 2 updated tests in test_factory.py. 260 tests passing (1 deselected), 91.75% coverage; ruff/format/mypy clean -- mypy needed one explicit cast, since build_messages()'s list[dict[str, str]] does not structurally match the SDK's ChatCompletionMessageParam TypedDict union. What is NOT done here, per the plan's own AI-04 acceptance ('manual call succeeds'): no real Groq key exists in this sandbox, so the one live call against the actual API has not been made. Left status in_progress rather than done until that human step happens.
- 2026-09-28: BE-07 closed out: the 249-test / 91.6%-coverage suite from the batched run above already exceeds the plan's 30+/>=70% acceptance bar, so the remaining work was tightening the enforced floor to match rather than adding tests for their own sake. Raised coverage.report.fail_under from 65 to 70 in backend/pyproject.toml, and the matching --cov-fail-under flag in ci.yml's test-backend job from 65 to 70, so both local and CI runs honestly enforce the plan's stated target instead of a looser placeholder. Reran the exact CI command afterward: 249 passed, 1 deselected, 91.59% coverage, comfortably above the new floor. The one remaining gap -- the integration-marked create-complaint test needing real Postgres/Redis -- is out of scope here: ci.yml's own comment assigns that to CI-02's Compose integration job (owner B), not to BE-07's testcontainers wiring, so conftest.py is left as-is.
- 2026-09-28: Timeline compressed to "finish tonight": dropped the week-based sequencing and batched seven tightly-coupled backend/AI tasks in one run instead of one task per PR -- AI-11 (provider factory), AI-10 (Redis outcome log + real /api/meta/providers), BE-03 (real ComplaintService, replacing the C0-05 stub routes), BE-04 (state machine + PATCH + optimistic-concurrency race guard), BE-06 (GracefulServer: SIGTERM flips readiness before uvicorn drains, not after), CA-02 (Redis fixed-window rate limiter, atomic INCR+EXPIRE via Lua), BE-08 (AST-based architecture test; OpenAPI 400 cleanup was already done by C0-05). Testing all seven together surfaced issues a one-task-at-a-time pass would have hit piecemeal anyway, worth listing because they explain real code choices: (1) the CA-02 tests need fakeredis's real Lua backend (`lupa`), missing from both this sandbox and the dev dependency group -- added it and regenerated uv.lock (uv itself had to be installed fresh here to do that). (2) mypy under the *actually pinned* SQLAlchemy 2.0.54 (this sandbox had drifted to 2.1.1 again) flagged a real bug in outcomes.py: redis-py 5.3.1's lrange() stub returns a union type that fails a bare `await`; fixed with an explicit Awaitable cast. (3) Two pre-existing observability tests (U8, I15) built their TestClient without entering the app lifespan, which the C0-05 stub routes never needed but the new real routes do -- fixed by entering it (U8) or faking the dependency directly (I15, since /health/ready/metrics are deliberately excluded from request-completed logging and can't stand in). (4) test_contract.py's create-complaint test now genuinely needs a live Postgres now that BE-03 wired the real service, and conftest.py has no testcontainers fixtures yet (that's BE-07/CI-02's job) -- marked it `integration` and excluded that marker in ci.yml's test-backend job rather than leave a test CI cannot actually pass. 249 tests passing (1 deselected), 91.6% coverage; ruff/format/mypy clean under the CI-accurate uv-managed venv; no OpenAPI drift.
- 2026-09-27: AI-07 + DOC-05: PII redaction (app/providers/triage/redaction.py::redact(), the plan's four patterns verbatim -- PK mobile, CNIC, email, house/plot address) and ADR 0004. Verified against the real seed data, not just hand-picked examples: three rows in app/seed/complaints.json actually contain a house number in text or location, and redact() catches all three. The ADR is written to distinguish what already exists (redact() itself, parsing.py's include_input=False) from what AI-04's not-yet-built GroqTriage is required to do (call redact(), never send reporter_contact/location) -- test A15 verifies that requirement once AI-04 lands. 14 tests (A14 parametrized over every pattern, plus that ordinary numbers and addresses are left alone).
- 2026-09-27: AI-06: prompt module (app/providers/triage/prompt.py, PROMPT_VERSION + SYSTEM + build_messages with delimiter neutralization) and the safety floor (_apply_safety_floor in triage_service.py): a HIGH_RISK keyword in the complaint text always forces priority=high, regardless of what the primary returned, applied on both a fresh primary success and a cache hit (proven with a cache seeded directly, bypassing write-time application, to show the read-time floor also catches it). A11 (the brief's injection test) needed no new mechanism at all: an LLM asked to return category='hacked' produces an invalid enum value, which is already MalformedOutput under AI-02/AI-03's existing validation, so it already falls back to rules -- the injection test is really proving the fallback path, not a new guardrail. 9 tests: A11, A12 (delimiter neutralization, both directions), A13 (safety floor overriding a valid-but-wrong low priority), plus that the floor leaves a correct high priority and ordinary text alone.
