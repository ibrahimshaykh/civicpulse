# Kubernetes manifests

`k8s/base/` -- namespace, ConfigMap, placeholder Secret, Postgres StatefulSet
+ PVC, Redis, backend/frontend Deployments (3 probes, preStop, requests/
limits), ClusterIP Services, Ingress (Traefik, `/api` -> backend, `/` ->
frontend), HPA v2 (with `behavior`), two PDBs, and a VPA in `updateMode: Off`
(recommendation-only -- needs the VPA CRDs/recommender installed in the
cluster to actually populate; this repo only ships the manifest).

`k8s/overlays/prod/` -- same manifests, image tags swapped for a specific
SHA at deploy time instead of the base's `:latest`:

```bash
cd k8s/overlays/prod
kustomize edit set image \
  ghcr.io/ibrahimshaykh/civicpulse-backend=ghcr.io/ibrahimshaykh/civicpulse-backend:$GIT_SHA \
  ghcr.io/ibrahimshaykh/civicpulse-frontend=ghcr.io/ibrahimshaykh/civicpulse-frontend:$GIT_SHA
kubectl apply -k .
```

## Quickstart (k3d)

```bash
k3d cluster create civicpulse
kubectl apply -k k8s/base
kubectl -n civicpulse get pods -w
```

The placeholder Secret ships with dummy values (`changeme`) -- replace them
for anything beyond a local demo:

```bash
kubectl -n civicpulse create secret generic civicpulse-secrets \
  --from-literal=POSTGRES_PASSWORD=<real value> \
  --from-literal=REDIS_PASSWORD=<real value> \
  --from-literal=GROQ_API_KEY=<real value> \
  --dry-run=client -o yaml | kubectl apply -f -
```

## Rollback (task K8-08)

Imperative:

```bash
kubectl -n civicpulse rollout undo deployment/backend
kubectl -n civicpulse rollout status deployment/backend
```

Declarative: revert the image tag in `k8s/overlays/prod/kustomization.yaml`
(or `git revert` the commit that bumped it) and re-apply:

```bash
kubectl apply -k k8s/overlays/prod
```

Not yet executed against a live cluster in this repo (no k3d/kind/minikube
available in the environment these manifests were written in) -- the
commands above are ready to run and validated structurally with
`kubectl kustomize` + `kubeconform`, but a real rollout/rollback demo still
needs to happen once a cluster exists, for the demo video (K8-08, task
DOC-10 segment 6) and rubric H1/H5/H6's live evidence.
