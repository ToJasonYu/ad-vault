# bidder-go

Real-time bidding engine. Given a user and a list of campaigns competing for their
impression, scores every candidate concurrently against `ml-service` and returns whichever
has the highest expected value (`click_probability * bid_amount`) — the standard ad-auction
notion of expected revenue.

Candidates are scored in parallel with goroutines rather than one at a time, since a live
bid request needs to resolve in milliseconds regardless of how many campaigns are competing.

## Setup

Requires `ml-service` running (see `ml-service/README.md`) — the bidder calls it for every
candidate score.

```
go run .
```

Listens on `:8080`. Override the ml-service address with `ML_SERVICE_URL` (defaults to
`http://127.0.0.1:8000`).

## Endpoints

- `GET /health` — liveness check
- `POST /bid` — body:
  ```json
  {
    "interest_segment": "sports",
    "device_type": "mobile",
    "age_bracket": "25-34",
    "candidates": [
      {"campaign_id": "camp_A", "category": "sports", "bid_amount": 2.00},
      {"campaign_id": "camp_B", "category": "finance", "bid_amount": 5.00}
    ]
  }
  ```
  returns the winning candidate with its click probability and expected value.
