# ml-service

Predicts click-through probability for a user+ad pair. A scikit-learn `LogisticRegression`
trained on the synthetic events from `data-generator/`, served over HTTP with FastAPI so the
Go bidding engine can call it during a live bid.

## Setup

```
pip install -r requirements.txt
```

Requires `data-generator/output/*.csv` to exist first — run the generator (see
`data-generator/README.md`) before training.

## Train

```
python train.py
```

Joins events with user and campaign attributes, adds a `segment_match` feature (does the
user's interest match the ad's category), trains a logistic regression pipeline, prints the
AUC on a held-out test split, then refits on the full dataset and saves it to `model.joblib`.
AUC is used instead of accuracy because clicks are rare (~3% CTR) — a model that never
predicts a click would score high on accuracy but be useless; AUC measures ranking quality
regardless of class imbalance.

## Serve

```
uvicorn app:app --port 8000
```

- `GET /health` — liveness check
- `POST /predict` — body: `{interest_segment, device_type, age_bracket, category, bid_amount}`,
  returns `{click_probability}`
