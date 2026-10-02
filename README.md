# Real-Time Hybrid Credit Card Fraud Detection & Risk Scoring

A machine learning project for detecting potentially fraudulent credit card transactions, translating model probabilities into an interpretable 0–100 risk score, and explaining predictions with SHAP.

**Live Dashboard:** https://fraud-detection-project-yqkkxiswxapfcqw63ggs84.streamlit.app/  
**GitHub Repository:** https://github.com/IshfaqCodes/fraud-detection-project

> Demo note: This is an educational demonstration using an anonymized public dataset. It is not a payment decision system and should not be used to make real financial decisions.

## Project Overview

The project combines a trained LightGBM classifier with risk scoring and explainability. It includes:

- Fraud probability prediction using the saved supervised model.
- Risk score and Low / Medium / High risk band.
- SHAP-based explanations for model outputs.
- FastAPI endpoints for prediction and health checks.
- Streamlit dashboard for interactive exploration.
- Notebooks covering data preparation, imbalance handling, model evaluation, explainability, risk scoring, experiment tracking, and monitoring.

## Live Demo

Open the [Fraud Detection Dashboard](https://fraud-detection-project-yqkkxiswxapfcqw63ggs84.streamlit.app/) in a browser. No local installation is required to view the hosted app. Free hosting services may sleep while idle, so the first request can take longer.

## Model Evaluation

The following are the validation-set metrics reported in the project (Notebook 04):

| Metric | LightGBM |
|---|---:|
| Precision | 0.944 |
| Recall | 0.718 |
| F1-score | 0.816 |
| ROC-AUC | 0.980 |
| PR-AUC | 0.825 |

Fraud is rare in the dataset (approximately 0.17% of transactions), so accuracy alone can be misleading. These figures are validation results, not a guarantee of performance on new data. Final test-set metrics are recorded in `models/final_test_evaluation.csv` after running the evaluation workflow.

## Technology Stack

- Python
- LightGBM and scikit-learn
- SHAP
- FastAPI and Uvicorn
- Streamlit
- MLflow
- pandas and NumPy
- Docker
- pytest

## Repository Structure

```text
.
├── data/
│   ├── README.md
│   └── processed/              # Prepared validation/test data
├── models/                     # Saved model and supporting artifacts
├── notebooks/                  # Project workflow notebooks (01–10)
├── scripts/
│   └── run_notebooks.py
├── src/
│   ├── main.py                 # FastAPI application
│   ├── dashboard.py            # Streamlit dashboard
│   ├── landing.py              # Dashboard landing page
│   ├── export_scaler.py
│   └── check_setup.py
├── tests/
│   └── test_api.py
├── Dockerfile.api
├── Dockerfile.dashboard
├── docker-compose.yml
├── requirements.txt
├── requirements-api.txt
├── requirements-dashboard.txt
└── requirements-notebooks.txt
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/IshfaqCodes/fraud-detection-project.git
cd fraud-detection-project
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

For the dashboard:

```bash
pip install -r requirements-dashboard.txt
```

For the API:

```bash
pip install -r requirements-api.txt
```

For notebook development:

```bash
pip install -r requirements-notebooks.txt
```

If you prefer the combined environment, use `pip install -r requirements.txt`.

### 4. Check project setup

```bash
python src/check_setup.py
```

The app requires the saved model and configuration artifacts under `models/`. Review `models/README.md` for artifact details.

## Run the Dashboard

```bash
streamlit run src/dashboard.py
```

Then open http://localhost:8501.

## Run the API

```bash
uvicorn src.main:app --reload
```

API documentation: http://127.0.0.1:8000/docs  
Health endpoint: http://127.0.0.1:8000/health

Use the Swagger UI to inspect and try the `POST /predict` endpoint.

## Run with Docker

```bash
docker compose up --build
```

When the containers are running:

- Dashboard: http://localhost:8501
- API docs: http://localhost:8000/docs

## Notebooks and Reproducibility

The `notebooks/` directory contains the project workflow, from exploration and preprocessing through evaluation, SHAP explainability, risk scoring, MLflow tracking, and monitoring.

Run notebooks in order where dependencies require it. In particular, the later evaluation/explainability/risk/experiment/monitoring stages are documented in `DEPLOY_FREE.md` and the notebook markdown. The full runner is:

```bash
python scripts/run_notebooks.py
```

Some early notebook steps require the original dataset and generated training split files.

## Dataset

The project is based on the public [Kaggle Credit Card Fraud Detection dataset](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud). The raw `creditcard.csv` is intentionally not included in this repository due to its size and dataset distribution terms.

To reproduce the data pipeline:

1. Obtain the dataset from Kaggle.
2. Place `creditcard.csv` at `data/creditcard.csv`.
3. Follow `data/README.md` and the notebook sequence.

Do not upload real customer or cardholder data to the public demo or repository.

## Testing

```bash
pytest tests -v
```

Tests may require project artifacts or dataset files; consult test output and project setup notes.

## Deployment

The hosted Streamlit dashboard is available at:

https://fraud-detection-project-yqkkxiswxapfcqw63ggs84.streamlit.app/

For deployment instructions and the optional API hosting workflow, see [`DEPLOY_FREE.md`](DEPLOY_FREE.md). The API should only be described as publicly deployed once its hosting URL has been configured and verified.

## Limitations and Responsible Use

- Predictions are model estimates, not proof that a transaction is fraudulent.
- Evaluation metrics depend on the dataset, split, threshold, and class distribution.
- SHAP explanations describe model behavior; they do not establish causation.
- Public demo hosting may sleep when inactive and may have resource limits.
- Do not submit real payment-card, customer, or other sensitive personal data.
- This project is intended for learning, portfolio demonstration, and experimentation—not production fraud prevention without independent validation, security review, privacy controls, monitoring, and operational safeguards.

## Author

**IshfaqCodes**  
GitHub: https://github.com/IshfaqCodes

---

If you find this project useful, feel free to explore the notebooks, inspect the implementation, or open an issue with suggestions.
