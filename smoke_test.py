"""Test a running local or Docker API: python smoke_test.py"""
import json
from urllib.request import Request, urlopen

def main():
    with urlopen("http://127.0.0.1:8000/health", timeout=10) as response:
        assert json.load(response) == {"status": "ok"}
    request = Request("http://127.0.0.1:8000/predict", data=json.dumps({
        "bhk": 2, "size": 1000, "bathroom": 2, "city": "Bangalore",
        "area_type": "Super Area", "furnishing_status": "Semi-Furnished"
    }).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=10) as response:
        result = json.load(response)
        assert result["predicted_rent"] > 0 and result["currency"] == "INR"
        print("PASS: health and prediction endpoints", result)

if __name__ == "__main__":
    main()
