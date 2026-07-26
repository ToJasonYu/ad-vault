# backoffice-rails

Advertiser back office: signup/login, campaign management, and budget tracking. A Rails
API-only app (no views/asset pipeline) — the React dashboard owns the UI, this just serves
JSON.

## Setup

```
bundle install
rails db:migrate
rails server -p 3000
```

## Auth

Signup and login return an `api_token`. Send it as `Authorization: Bearer <token>` on every
other request. `POST /events` is the exception — it's called by the client-side event logger,
not the advertiser, so it isn't gated behind the advertiser's token (same as a real-world
tracking pixel).

## Endpoints

- `POST /signup` — `{name, email, password}` -> advertiser + token
- `POST /login` — `{email, password}` -> advertiser + token
- `GET /campaigns`, `GET /campaigns/:id` — list/show the current advertiser's campaigns
- `POST /campaigns` — `{name, category, budget, bid_amount}`
- `PATCH /campaigns/:id` — update a campaign
- `POST /events` — `{campaign_id, event_type}` (`impression` or `click`); a `click` decrements
  the campaign's `budget_remaining` by its `bid_amount`, floored at 0. No real payment
  processor — budget is just a number that goes down, by design.
