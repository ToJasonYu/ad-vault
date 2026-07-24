import os

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.joblib")

app = FastAPI(title="ad-vault ml-service")
model = joblib.load(MODEL_PATH)


class PredictRequest(BaseModel):
    interest_segment: str
    device_type: str
    age_bracket: str
    category: str
    bid_amount: float


class PredictResponse(BaseModel):
    click_probability: float


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    # segment_match is derived, not sent by the caller - keeps the API
    # contract in terms of raw user+ad attributes, not internal features
    segment_match = int(request.interest_segment == request.category)

    row = pd.DataFrame([{
        "interest_segment": request.interest_segment,
        "device_type": request.device_type,
        "age_bracket": request.age_bracket,
        "category": request.category,
        "bid_amount": request.bid_amount,
        "segment_match": segment_match,
    }])

    probability = model.predict_proba(row)[0, 1]

    return PredictResponse(click_probability=float(probability))
