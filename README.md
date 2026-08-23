# Ad-vault

Ad-vault is a multi-service ad-recommendation platform. It
demonstrates an end-to-end ad-tech architecture spanning real-time bidding, machine-learned
click-through-rate prediction, an advertiser back office, client-side event logging, and
container orchestration with Kubernetes. Each service is implemented in a different language
and framework, chosen to match how these systems are typically built in production.

## Tech stack

| Layer | Technology |
|---|---|
| Real-time bidding engine | Go, standard library `net/http` |
| Click-through-rate prediction | Python, scikit-learn (Logistic Regression), FastAPI |
| Advertiser back office / API | Ruby on Rails (API-only) |
| Advertiser dashboard | React (Vite) |
| Client-side event logging | Kotlin (JVM) |
| Container orchestration | Docker, Kubernetes |
| Synthetic data generation | Python |

## Architecture

```
                        ┌─────────────────────┐
                        │   data-generator     │  synthetic advertisers, campaigns,
                        │      (Python)        │  users, impressions, clicks
                        └──────────┬───────────┘
                                   │ seeds
                                   ▼
        ┌───────────────────────────────────────────────┐
        │              backoffice-rails (Ruby)           │
        │  advertiser signup, campaign CRUD, budget       │
        │  tracking (decrements only, no real payments)   │
        └───────────────────┬─────────────┬──────────────┘
                             │             │
                    reads/writes API   serves dashboard data
                             │             │
                             ▼             ▼
              ┌───────────────────┐  ┌──────────────────────┐
              │ event-logger-      │  │  dashboard-react      │
              │ kotlin             │  │  create campaigns,     │
              │ logs impressions/  │  │  view impressions/     │
              │ clicks             │  │  clicks/spend           │
              └─────────┬──────────┘  └───────────────────────┘
                        │
                        │ future training data
                        ▼
              ┌───────────────────┐        ┌─────────────────────┐
              │   bidder-go        │──────▶│    ml-service         │
              │ real-time bidding  │  calls │  scikit-learn         │
              │ engine, ms-scale   │◀──────│  LogisticRegression    │
              │                    │ score  │  CTR model, FastAPI    │
              └───────────────────┘        └─────────────────────┘

                        infra-k8s orchestrates all of the above:
                        restart, scale, service discovery (no business logic)
```

## System behavior

1. **data-generator** produces a synthetic advertising dataset: advertisers, campaigns,
   users, and a history of impression and click events. Click behavior is not random —
   users have an interest segment, campaigns have a category, and matching the two
   increases click probability. This gives the prediction model a genuine, learnable
   pattern rather than pure noise.

2. When a bid request arrives, **bidder-go** queries **ml-service** for a click-probability
   score on each candidate ad, ranks candidates by expected value (click probability
   multiplied by bid amount), and returns the winning ad. Candidate scoring is performed
   concurrently so the request resolves in milliseconds regardless of how many campaigns are
   competing.

3. When an ad is served and, in some cases, clicked, **event-logger-kotlin** — representing
   client-side instrumentation — records the impression or click by calling
   **backoffice-rails**'s event endpoint. These events update campaign budgets in real time
   and are intended to become future training data for the prediction model.

4. **backoffice-rails** is the advertiser-facing API: account signup and authentication,
   campaign creation, and budget tracking. A campaign's remaining budget decrements as click
   events are recorded. There is no real payment processor; budget is tracked purely as a
   number in the database, which is an intentional scope reduction for this project.

5. **dashboard-react** is the advertiser-facing web application: creating campaigns and
   monitoring impressions, clicks, and spend as they accumulate.

6. **infra-k8s** contains the Kubernetes manifests that run the containerized services,
   handling restarts, scaling, and service discovery. This layer is strictly infrastructure
   and contains no application logic.

## Services

| Directory | Stack | Responsibility |
|---|---|---|
| `data-generator/` | Python | Generates synthetic advertisers, campaigns, users, and events with a learnable click-through signal |
| `ml-service/` | Python, FastAPI, scikit-learn | Trains and serves a click-through-rate prediction model, evaluated with AUC |
| `bidder-go/` | Go | Real-time bidding engine; scores candidate ads via `ml-service` and returns the winning bid |
| `backoffice-rails/` | Ruby on Rails (API-only) | Advertiser authentication, campaign management, and budget tracking |
| `dashboard-react/` | React (Vite) | Advertiser dashboard for campaign management and performance reporting |
| `event-logger-kotlin/` | Kotlin | Client-side impression and click event logging |
| `infra-k8s/` | Kubernetes manifests | Deployment, service discovery, scaling, and restart policy for the containerized services |

Each directory contains its own README with setup and run instructions specific to that
service.

## Design decisions and scope

This project intentionally limits scope in a few places, to keep the system focused on
demonstrating architecture rather than reproducing every feature of a production ad
platform:

- **No payment processing.** Campaign budgets are tracked as a plain decrementing value in
  the database rather than integrating a real payment provider.
- **Token-based authentication.** `backoffice-rails` uses `has_secure_password` and an
  issued API token rather than a third-party authentication gem, to keep the authentication
  logic transparent and self-contained.
- **Development-mode Rails container.** The `backoffice-rails` Docker image runs in
  development mode; a production deployment would require injecting `RAILS_MASTER_KEY` as a
  Kubernetes secret and switching to a persistent database such as PostgreSQL, since the
  containerized SQLite database does not persist across pod restarts.
- **Build-time API configuration for the dashboard.** `dashboard-react`'s API base URL is
  set at image build time, since Vite environment variables are resolved at compile time. A
  production deployment would front the API with an Ingress and a stable domain instead.
- **No Ingress or TLS.** Local verification of the containerized services was done with
  `kubectl port-forward` rather than an Ingress controller.

## Verification

Every service in this project was exercised end to end rather than assumed to work from
code review alone:

- The prediction model's AUC (~0.73) was measured against a held-out test split, confirming
  the model learns real signal rather than memorizing noise.
- The bidding engine was tested against a live `ml-service` instance and confirmed to select
  the correct winning candidate based on expected value, not simply the highest bid.
- The Rails API was tested for signup, duplicate-account rejection, authentication, scoped
  campaign access, and budget decrementing on click events.
- The event logger was run against a live Rails instance and confirmed to produce the
  expected budget change.
- The dashboard's data layer was exercised against a live Rails instance, covering
  authentication, campaign creation, and scoped campaign listing.
- All four containerized services were deployed to a local Kubernetes cluster (via `kind`),
  with cross-service communication verified over cluster DNS, along with scaling and
  automatic pod recreation on failure.
