# ad-vault

A mini ad-recommendation platform, built as a portfolio project to demonstrate a realistic
multi-service ad-tech stack: real-time bidding, ML-based click prediction, an advertiser
back office, a client-side event logger, and Kubernetes orchestration tying it together.

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

## Data flow, in plain terms

1. **data-generator** fabricates a fake ad ecosystem: advertisers, campaigns, users, and a
   history of impression/click events. The click behavior isn't random — certain user
   segments genuinely prefer certain ad categories, so the ML model has real signal to learn
   from instead of noise.
2. A real-time **bid request** arrives at the **bidder-go** engine. It asks the
   **ml-service** for a click-probability score for candidate ads, picks the highest-scoring
   ad, and returns it — all within milliseconds.
3. When an ad is shown and (maybe) clicked, the **event-logger-kotlin** client records that
   impression/click, writing it to the Rails database and, eventually, back into the training
   data for the ML model.
4. **backoffice-rails** is where advertisers sign up, create campaigns, and set budgets.
   Budgets decrement as impressions/clicks happen — there's no real payment processor,
   that's an intentional scope cut.
5. **dashboard-react** is the advertiser-facing UI: create campaigns, watch
   impressions/clicks/spend roll in.
6. **infra-k8s** holds the Kubernetes manifests that run all of the above as containers,
   handling restarts, scaling, and service discovery. It contains no business logic itself.

## Directory structure

| Directory | Language | Purpose |
|---|---|---|
| `data-generator/` | Python | Synthetic advertisers/campaigns/users/events with learnable signal |
| `ml-service/` | Python (FastAPI, scikit-learn) | CTR prediction: click probability from user+ad features, evaluated with AUC |
| `bidder-go/` | Go | Real-time bidding engine, calls ml-service, returns winning ad |
| `backoffice-rails/` | Ruby (Rails) | Advertiser signup, campaign creation, budget tracking |
| `dashboard-react/` | React | Advertiser dashboard UI |
| `event-logger-kotlin/` | Kotlin | Client-side impression/click event logging |
| `infra-k8s/` | Kubernetes manifests | Container orchestration for all services |

## Status

Under active development. See commit history for progress; each service directory will get
its own README with setup/run instructions as it's built out.
