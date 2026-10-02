# Real-Time Hybrid Credit Card Fraud Detection & Risk Scoring

Detects fraudulent credit card transactions with a LightGBM model, converts the fraud probability into a
0-100 risk score (Low / Medium / High), explains each decision with SHAP, and serves it through a
FastAPI service and a Streamlit dashboard. Includes MLflow tracking and drift monitoring.

## Saved model (for deployment)

`models/best_supervised_model.pkl` - the trained LightGBM model (joblib format).
Details and a loading example: [models/README.md](models/README.md).

## Project structure

```
data/         creditcard.csv (download, see data/README.md) and data/processed/ train/val/test splits
notebooks/    01-10: EDA, preprocessing, imbalance, models, evaluation, SHAP, risk scoring, MLflow, monitoring
src/          main.py (FastAPI), dashboard.py + landing.py (Streamlit), export_scaler.py, check_setup.py
models/       trained model and all saved artifacts
scripts/      run_notebooks.py (executes notebooks 06-10 in order)
tests/        API tests (pytest)
```

## Setup (Windows / macOS / Linux, Python 3.12 recommended)

```bash
git clone <repository-url>
cd fraud_detection_project

python -m venv .venv
# Windows:    .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements-notebooks.txt
```

Download `creditcard.csv` from Kaggle (https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
and place it at `data/creditcard.csv`. It is not stored in the repository because it is larger than
GitHub's 100 MB file limit.

Verify the setup:

```bash
python src/check_setup.py
```

## Run the notebooks

Open `notebooks/` in VS Code or Jupyter (`jupyter lab`) and run notebooks **06 -> 07 -> 08 -> 09 -> 10 in
that order**, "Run All" in each. Or run them all from the terminal:

```bash
python scripts/run_notebooks.py
```

Order matters: 06 writes `threshold_config.pkl` (read by 07, 08, 09) and 08 writes
`risk_scoring_config.pkl` (read by the API and dashboard). Notebooks 01-05 are the earlier phases
(they need `X_train.csv`; run notebook 02 first to regenerate it from `creditcard.csv`).
Notebook 09 creates `mlflow.db` / `mlruns/` locally; view them with
`mlflow ui --backend-store-uri sqlite:///mlflow.db` (http://127.0.0.1:5000).

## Run the API

```bash
uvicorn src.main:app --reload
```

Open http://127.0.0.1:8000/docs, try `POST /predict` (the example payload is pre-filled), or `GET /health`.

## Run the dashboard

```bash
streamlit run src/dashboard.py
```

Opens at http://localhost:8501.

## Run the tests

```bash
pytest tests -v
```

(Needs `data/creditcard.csv`; the tests are skipped with a message if it is missing.)

## Docker

```bash
docker compose up --build
```

API -> http://localhost:8000/docs, Dashboard -> http://localhost:8501.

## Model performance (validation set, notebook 04)

| Metric | LightGBM |
|--------|----------|
| Precision | 0.944 |
| Recall | 0.718 |
| F1 | 0.816 |
| ROC-AUC | 0.980 |
| PR-AUC | 0.825 |

Fraud is only ~0.17% of transactions, so accuracy is misleading; precision/recall/PR-AUC are reported instead.
Final test-set numbers are written by notebook 06 to `models/final_test_evaluation.csv`.

## Free online deployment

Step-by-step guide (Streamlit Community Cloud for the dashboard, Render for the API): [DEPLOY_FREE.md](DEPLOY_FREE.md).

See `INSTRUCTIONS.md` for the phase-by-phase history of the project.
