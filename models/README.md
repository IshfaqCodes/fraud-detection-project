# Saved models and artifacts

## The deployable model

**`best_supervised_model.pkl`** is the trained champion model: a LightGBM classifier
(`LGBMClassifier`), saved with `joblib`. This is the file used in production by the API
(`src/main.py`) and the dashboard (`src/dashboard.py`).

Test-set results for the champion are produced by notebook 06 (`final_test_evaluation.csv`).
Validation results (notebook 04): precision 0.944, recall 0.718, F1 0.816, ROC-AUC 0.980, PR-AUC 0.825.
Plain "accuracy" is not reported because only ~0.17% of transactions are fraud (a model that
flags nothing already scores above 99%), so precision, recall and PR-AUC are the meaningful metrics.

Load and predict:

```python
import joblib, pandas as pd
model = joblib.load("models/best_supervised_model.pkl")
X = pd.read_csv("data/processed/X_test.csv").head(5)   # 30 features: V1-V28, Amount_scaled, Time_scaled
print(model.predict_proba(X)[:, 1])                    # fraud probability
```

The pickle was created with scikit-learn 1.8.0 and lightgbm 4.7.0; install the pinned versions
from `requirements-api.txt` to load it without warnings.

## Other files

| File | Created by | Used by |
|------|-----------|---------|
| `isolation_forest.pkl`, `hybrid_config.pkl` | notebook 05 | notebooks 06, 09 |
| `threshold_config.pkl`, `final_test_evaluation.csv`, `threshold_optimization_comparison.csv` | notebook 06 | notebooks 07, 08, 09 |
| `shap_feature_importance.csv` | notebook 07 | dashboard |
| `risk_scoring_config.pkl`, `risk_scored_test_sample.csv` | notebook 08 | API, dashboard |
| `scaler_params.json` | `python src/export_scaler.py` | API, dashboard |
| `monitoring_baseline.pkl`, `drift_report_baseline.csv` | notebook 10 | drift checks |
| `*_comparison.csv` | notebooks 03-05 | notebook 09 |
