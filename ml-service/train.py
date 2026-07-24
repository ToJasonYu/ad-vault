import os

import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data-generator", "output")
FEATURE_COLUMNS = ["interest_segment", "device_type", "age_bracket", "category", "bid_amount", "segment_match"]
LABEL_COLUMN = "clicked"


def load_data():
    events = pd.read_csv(os.path.join(DATA_DIR, "events.csv"))
    users = pd.read_csv(os.path.join(DATA_DIR, "users.csv"))
    campaigns = pd.read_csv(os.path.join(DATA_DIR, "campaigns.csv"))

    return events, users, campaigns


def build_features(events, users, campaigns):
    merged = events.merge(users, on="user_id").merge(campaigns, on="campaign_id")
    merged["segment_match"] = (merged["interest_segment"] == merged["category"]).astype(int)

    X = merged[FEATURE_COLUMNS]
    y = merged[LABEL_COLUMN]

    return X, y


def main():
    events, users, campaigns = load_data()
    X, y = build_features(events, users, campaigns)

    print(f"training rows: {len(X)}")
    print(f"overall CTR: {y.mean():.4f}")
    print(X.head())


if __name__ == "__main__":
    main()
