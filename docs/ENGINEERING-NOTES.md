# Engineering Notes

## Eight Questions
1. **Three things that differ:** Network (localhost vs docker bridge), secrets (local .env vs GH secrets), filesystem (local vs ephemeral runner). Dockerfile freeze: `COPY . .` vs explicit copying. Manifest freeze: `imagePullPolicy`.
2. **CI/CD Maturity:** Level 2 (Automated deployment). Next rung: Level 3 (Automated canary analysis), buys zero-downtime safety.
3. **Build-once-deploy-many:** `compose.prod.yaml` uses `image: ${IMAGE_TAG}` instead of `build:`. Breaks if frontend config is baked in.
4. **Deterministic LLM testing:** We inject a `SimulatedTriage` provider in CI which returns seeded deterministic data, so tests don't flake.
5. **HPA lag:** ~30-45s lag between load and capacity. Time goes to metric gathering and pod startup. Reduced by lowering `stabilizationWindowSeconds`.
6. **VPA Off mode:** VPA runs in Off (Recommender) mode because Auto mode adjusts CPU requests, which changes the denominator for HPA, causing conflict where HPA scales down and VPA scales up.
7. **Network internal true:** Backend is bridged to both `edge` and `internal`. It reaches LLM API via external network egress, while DB/Cache sit on `internal`.
8. **The failure:** In week 2, tests failed sporadically. Believed it was race conditions, but log line `Connection refused` showed Redis mock wasn't tearing down properly between tests.

## Other Constraints
- **Merge conflict:** Resolved config.py by keeping LLM parameters and retaining DB pool size = 5.
- **Indexes:** `idx_status` for filtering Dashboard by status, `idx_created_at` for sorting pagination.
- **AOF Volume:** AOF persistence for Redis ensures rate limit buckets and cached triage outcomes survive a pod restart, preventing quota bursts.
- **Deviations:** SimulatedTriage was added to allow robust CI testing without real LLM keys.
