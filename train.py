"""Run: python train.py. Saves preprocessing and trained model together."""
import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ROOT = Path(__file__).resolve().parent
FEATURES = ["BHK", "Size", "Bathroom", "City", "Area Type", "Furnishing Status"]

def train():
    data = pd.read_csv(ROOT / "data/House_Rent_Dataset.csv").drop_duplicates()
    X, y = data[FEATURES], data["Rent"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    # Fit encoding ONLY on the training data to avoid test-data leakage.
    preprocess = ColumnTransformer([
        ("categories", OneHotEncoder(handle_unknown="ignore"), FEATURES[3:]),
        ("numbers", "passthrough", FEATURES[:3]),
    ])
    parameters = dict(n_estimators=100, max_depth=12, min_samples_leaf=2,
                      random_state=42, n_jobs=1)
    model = Pipeline([("preprocess", preprocess),
                      ("regressor", RandomForestRegressor(**parameters))])
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    baseline = DummyRegressor(strategy="median").fit(X_train, y_train)
    metrics = {
        "train_rows": len(X_train), "test_rows": len(X_test),
        "mae_inr": float(mean_absolute_error(y_test, predictions)),
        "rmse_inr": float(np.sqrt(mean_squared_error(y_test, predictions))),
        "r2": float(r2_score(y_test, predictions)),
        "baseline_mae_inr": float(mean_absolute_error(y_test, baseline.predict(X_test))),
        "test_size": 0.2, "random_state": 42,
    }
    joblib.dump(model, ROOT / "model.joblib", compress=3)
    (ROOT / "parameters.json").write_text(json.dumps(parameters, indent=2))
    (ROOT / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))
    print("Saved model.joblib, parameters.json and metrics.json")
    return model, metrics

if __name__ == "__main__":
    train()
