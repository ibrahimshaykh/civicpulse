# CivicPulse Runbook

## Deploy
Deployments are handled by CD via GitHub Actions. Merging to `main` triggers a deploy to the cluster using the built SHA.

## Rollback
Imperative:
`kubectl rollout undo deployment/backend -n civicpulse`

Declarative:
Revert the commit or modify `k8s/overlays/prod/kustomization.yaml` to point to a previous stable SHA and apply.

## Reading Logs
`kubectl logs -l app=backend -n civicpulse -f`

## What to do when triage starts failing
1. Check `/api/meta/providers` to see the active provider and error classes.
2. If `rules:fallback` is triggering, check Groq API key validity and quota.
3. Check Redis connection using `kubectl logs -l app=redis -n civicpulse`.
