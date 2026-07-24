import os

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data-generator", "output")
CATEGORICAL_COLUMNS = ["interest_segment", "device_type", "age_bracket", "category"]
NUMERIC_COLUMNS = ["bid_amount", "segment_match"]
FEATURE_COLUMNS = CATEGORICAL_COLUMNS + NUMERIC_COLUMNS
LABEL_COLUMN = "clicked"
TEST_SIZE = 0.2
RANDOM_STATE = 42
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.joblib")


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


def build_model():
    preprocessor = ColumnTransformer([
        ("onehot", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_COLUMNS),
    ], remainder="passthrough")

    return Pipeline([
        ("preprocess", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000)),
    ])


def main():
    events, users, campaigns = load_data()
    X, y = build_features(events, users, campaigns)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    model = build_model()
    model.fit(X_train, y_train)

    predicted_probs = model.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, predicted_probs)

    print(f"training rows: {len(X_train)}, test rows: {len(X_test)}")
    print(f"test AUC: {auc:.4f}")

    # AUC is measured on the held-out split; refit on everything before shipping the model
    final_model = build_model()
    final_model.fit(X, y)
    joblib.dump(final_model, MODEL_PATH)
    print(f"saved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
