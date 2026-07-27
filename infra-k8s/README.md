# infra-k8s

Kubernetes manifests for `bidder-go`, `ml-service`, `backoffice-rails`, and `dashboard-react`
— one Deployment + Service each, plus a shared `ad-vault-config` ConfigMap that gives
`bidder-go` the cluster-internal DNS name for `ml-service`. Infra only, no business logic.

`event-logger-kotlin` isn't deployed here — it represents client-side code that runs on an
end user's device, not a backend service. `data-generator` is a one-off script, not a
long-running process, so it isn't deployed either.

## Try it locally with kind

Requires Docker and [kind](https://kind.sigs.k8s.io/).

```
# build all four images (from the repo root)
docker build -t ad-vault/bidder-go:latest bidder-go
docker build -f ml-service/Dockerfile -t ad-vault/ml-service:latest .
docker build -t ad-vault/backoffice-rails:latest backoffice-rails
docker build -t ad-vault/dashboard-react:latest dashboard-react

kind create cluster --name ad-vault
kind load docker-image ad-vault/bidder-go:latest ad-vault/ml-service:latest \
  ad-vault/backoffice-rails:latest ad-vault/dashboard-react:latest --name ad-vault

kubectl apply -f infra-k8s/
kubectl -n ad-vault get pods
```

`kind load docker-image` (rather than a registry push) is what makes locally-built images
available to the cluster's nodes — that's why every Deployment sets
`imagePullPolicy: IfNotPresent`, so Kubernetes doesn't try to pull `ad-vault/*` from Docker
Hub, where it doesn't exist.

## Verifying service discovery

The interesting part isn't that the pods start — it's that `bidder-go` can reach
`ml-service` purely through cluster DNS, with no hardcoded IPs:

```
kubectl -n ad-vault run debug --image=curlimages/curl --restart=Never --rm -i --command -- \
  curl -s -X POST http://bidder-go:8080/bid -H "Content-Type: application/json" \
  -d '{"interest_segment":"sports","device_type":"mobile","age_bracket":"25-34","candidates":[{"campaign_id":"camp_A","category":"sports","bid_amount":2.00}]}'
```

Restart and scaling both come from Kubernetes itself, not app code:
`kubectl -n ad-vault scale deployment bidder-go --replicas=2`, or delete a pod and watch the
Deployment recreate it.

## Known simplifications

- `backoffice-rails` runs in development mode in-cluster — production would need
  `RAILS_MASTER_KEY` injected as a real Kubernetes Secret, and Postgres instead of SQLite
  (SQLite lives inside the container, so it's wiped on every pod restart).
- `dashboard-react`'s API URL is baked in at image build time (`VITE_API_BASE_URL`), since
  Vite env vars are compile-time. A real deployment would front the API with an Ingress and a
  real domain instead of relying on a build-time constant.
- No Ingress, TLS, or persistent volumes — reaching `backoffice-rails` or `dashboard-react`
  from outside the cluster during local testing was done with `kubectl port-forward`.
