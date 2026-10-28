# House Rent Prediction — start here

A simple college project: CSV → Random Forest → model.joblib → FastAPI → Docker → GitHub Actions.

## What is already done

- Your dataset: 4,746 rows, 12 columns; no missing values or duplicate rows found.
- Trained locally with Python 3.12: 3,796 training rows and 950 test rows (80/20 split, seed 42).
- Saved `model.joblib`: fitted encoder, trained trees and model settings together.
- Saved readable settings in `parameters.json` and test results in `metrics.json`.
- Local API tests: **3 passed**. Live HTTP health and prediction requests also passed.
- Colab notebook, Dockerfile and GitHub Actions workflow are ready.
- **Not executed here:** Colab session, Docker container, repository creation or a hosted GitHub Actions run. Docker is unavailable in this environment; the connected GitHub integration cannot create repositories. A green hosted pipeline is not yet verified.

## 1. Dataset

The supplied Kaggle ZIP contained `House_Rent_Dataset.csv` and its glossary. Both are in `data/`. Keep your original Kaggle dataset link for your report; the ZIP did not include a source URL or licence. Check the dataset's sharing terms before making the repository public.

Inputs: BHK, Size (square feet), Bathroom, City, Area Type, Furnishing Status.
Target: Rent (INR). Date, locality, floor, tenant preference and contact details are excluded to keep the demonstration small. The source dates are from 2022, so this is an educational model, not a current rental quotation.

## 2–3. Train on Colab and save the model

1. Open https://colab.research.google.com/ and use **File → Upload notebook**.
2. Choose `House_Rent_Colab.ipynb` from this extracted project.
3. Run the first cell and upload the original `house-rent-prediction.zip` supplied with this project.
4. Run the remaining cells in order. Training takes a short time. If Colab requests a runtime restart after installation, restart and rerun the cells.
5. The last cell downloads `house-rent-trained.zip` containing your newly trained model and project. Extract it for VS Code.

`model.joblib` is already supplied so you can demonstrate the API immediately, but run Colab yourself to satisfy the Colab requirement and capture a screenshot of the metrics.

## 4. Run in VS Code (Windows)

Install Python 3.12 and VS Code. Open the extracted **house-rent-prediction** folder (the folder containing `app.py`). In VS Code, choose Terminal → New Terminal. Run these PowerShell commands one at a time:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m uvicorn app:app --reload
```

No environment activation is needed. On macOS/Linux, use `python3.12 -m venv .venv` and replace `.venv\Scripts\python.exe` with `.venv/bin/python`.

Open http://127.0.0.1:8000/docs in your browser.

- **GET /**: project message.
- **GET /health**: confirms the running application loaded its model.
- **POST /predict**: click **Try it out**, paste this JSON, and click **Execute**:

```json
{
  "bhk": 2,
  "size": 1000,
  "bathroom": 2,
  "city": "Bangalore",
  "area_type": "Super Area",
  "furnishing_status": "Semi-Furnished"
}
```

A successful response has `predicted_rent` and `currency: "INR"`. Negative size, missing fields and unsupported cities produce HTTP 422.

To retrain locally if needed:

```powershell
.venv\Scripts\python.exe train.py
```

Stop the server with **Ctrl+C** before using Docker on the same port.

## 5. Execute the endpoints through Docker

Install and start Docker Desktop. Wait until its engine is running. From the same project folder:

```powershell
docker build -t house-rent-api .
docker run --rm --name rent-api -p 8000:8000 house-rent-api
```

Open http://127.0.0.1:8000/docs and execute the same endpoints. In a second terminal you can also run:

```powershell
.venv\Scripts\python.exe smoke_test.py
```

This time requests reach the API inside Docker. Take a screenshot of the prediction response and the running container. Stop with Ctrl+C. The Docker image copies the saved model; it does not retrain on startup.

## 6. Create a GitHub repository

1. Sign in at https://github.com/new.
2. Repository name: `house-rent-prediction`. Choose **Private** for the classroom project initially.
3. Leave README, .gitignore and licence unchecked, then click **Create repository**.
4. Install Git if needed. In the VS Code project terminal:

```powershell
git init
git add .
git commit -m "Add house rent prediction project"
git branch -M main
git remote add origin https://github.com/SinghhSarvesh/house-rent-prediction.git
git push -u origin main
```

If Git asks for identity, configure your own name and email using `git config --global user.name` and `git config --global user.email`, then retry the commit. Complete GitHub's browser sign-in when prompted. If the repository name already exists, choose another name and use its exact URL in `git remote add origin`.

Do not upload only the ZIP: the workflow must exist at `.github/workflows/ci.yml` in the repository. `git add .` includes that folder automatically.

## 7–8. Run and verify GitHub Actions

The included `.github/workflows/ci.yml` starts on each push, pull request or manual run. It:

1. Checks out your code and installs Python 3.12 dependencies.
2. Trains the model and saves it.
3. Runs the three automated API tests.
4. Builds and starts Docker.
5. Checks health and prediction over HTTP through the container.
6. Shows logs and removes the container.

Open your repository → **Actions → House Rent CI → latest run**. Wait for all steps to finish. **Only a green successful run confirms step 8.** Open the run and take a screenshot for your submission. If it fails, open the first red step and read its error; don't treat a local test pass as a hosted CI pass. If Actions are disabled, enable them in repository settings. A private account may need available Actions minutes.

This is CI (automatic validation), not deployment to a public hosting service.

## Results and limitations

| Metric | Held-out result |
|---|---:|
| MAE | ₹13,305.51 |
| RMSE | ₹36,832.08 |
| R² | 0.6596 |
| Median baseline MAE | ₹24,269.46 |

MAE is the average absolute prediction error. RMSE gives more weight to large mistakes. R² is a regression score, **not 65.96% accuracy**. High-rent outliers can cause large errors. These scores use one fixed random test split, without tuning against the test set. Individual predictions can be substantially wrong.

## Files you should understand

| File | Purpose |
|---|---|
| `House_Rent_Colab.ipynb` | Colab upload, training, evaluation and download |
| `train.py` | Train/test split, encoding, Random Forest and saving |
| `model.joblib` | Saved fitted pipeline |
| `parameters.json` | Readable Random Forest settings |
| `metrics.json` | Actual held-out model results |
| `app.py` | FastAPI endpoints and input validation |
| `tests/test_api.py` | Health, prediction consistency and invalid-input tests |
| `smoke_test.py` | HTTP checks against a running server/container |
| `Dockerfile` | Container image recipe |
| `.github/workflows/ci.yml` | Automated training, tests and Docker checks |
| `VIVA.md` | Short explanation and common questions |

Use the pinned requirements in Colab and VS Code/Docker to keep model versions consistent. Load only your own trusted joblib files.

Reference documentation: https://scikit-learn.org/stable/model_persistence.html and https://docs.github.com/en/actions/tutorials/build-and-test-code/python.
