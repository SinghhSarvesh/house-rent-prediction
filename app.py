from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI(title="House Rent Prediction", version="1.0")

# Load the saved model from the same folder as app.py
model = joblib.load(Path(__file__).with_name("model.joblib"))


# Define the input fields and their validation rules
class House(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "bhk": 2,
                "size": 1000,
                "bathroom": 2,
                "city": "Bangalore",
                "area_type": "Super Area",
                "furnishing_status": "Semi-Furnished",
            }
        },
    )

    bhk: int = Field(ge=1, le=6)
    size: float = Field(gt=0, le=10000, allow_inf_nan=False)
    bathroom: int = Field(ge=1, le=10)

    city: Literal[
        "Kolkata", "Mumbai", "Bangalore",
        "Delhi", "Chennai", "Hyderabad"
    ]
    area_type: Literal["Super Area", "Carpet Area", "Built Area"]
    furnishing_status: Literal[
        "Unfurnished", "Semi-Furnished", "Furnished"
    ]


@app.get("/")
def home():
    return {"message": "House Rent Prediction API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(house: House):
    # Column names must match those used during training
    data = pd.DataFrame([{
        "BHK": house.bhk,
        "Size": house.size,
        "Bathroom": house.bathroom,
        "City": house.city,
        "Area Type": house.area_type,
        "Furnishing Status": house.furnishing_status,
    }])

    rent = float(model.predict(data)[0])

    return {
        "predicted_rent": round(rent, 2),
        "currency": "INR",
    }