import math
import joblib
import pandas as pd
from fastapi.testclient import TestClient
from app import app
from train import ROOT

HOUSE = {"bhk": 2, "size": 1000, "bathroom": 2, "city": "Bangalore",
         "area_type": "Super Area", "furnishing_status": "Semi-Furnished"}

def test_health():
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}

def test_prediction_matches_saved_model():
    model = joblib.load(ROOT / "model.joblib")
    row = pd.DataFrame([[2, 1000, 2, "Bangalore", "Super Area", "Semi-Furnished"]],
                       columns=["BHK", "Size", "Bathroom", "City", "Area Type", "Furnishing Status"])
    expected = round(float(model.predict(row)[0]), 2)
    with TestClient(app) as client:
        response = client.post("/predict", json=HOUSE)
        assert response.status_code == 200
        assert response.json() == {"predicted_rent": expected, "currency": "INR"}
        assert math.isfinite(expected) and expected > 0

def test_invalid_inputs():
    with TestClient(app) as client:
        for field, value in [("size", -1), ("bhk", 0), ("city", "Unknown")]:
            assert client.post("/predict", json={**HOUSE, field: value}).status_code == 422
        assert client.post("/predict", json={}).status_code == 422
