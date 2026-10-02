"""Quick health check: are all files needed to run the project present, and does the model load?

Run from the project root:  python src/check_setup.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED = {
    "models/best_supervised_model.pkl": "trained LightGBM model (the deployable file)",
    "models/risk_scoring_config.pkl": "risk-band thresholds (notebook 08)",
    "models/scaler_params.json": "Amount/Time scaler (python src/export_scaler.py)",
    "data/processed/X_val.csv": "validation features (notebook 02)",
    "data/processed/X_test.csv": "test features (notebook 02)",
    "data/processed/y_val.csv": "validation labels (notebook 02)",
    "data/processed/y_test.csv": "test labels (notebook 02)",
}
OPTIONAL = {
    "data/creditcard.csv": "raw dataset - needed for notebook 06 and tests/ (see data/README.md)",
    "models/threshold_config.pkl": "created by notebook 06",
    "models/final_test_evaluation.csv": "created by notebook 06",
}


def main() -> int:
    ok = True
    for rel, why in REQUIRED.items():
        found = (ROOT / rel).exists()
        ok &= found
        print(f"[{'OK' if found else 'MISSING'}] {rel}  - {why}")
    for rel, why in OPTIONAL.items():
        print(f"[{'OK' if (ROOT / rel).exists() else 'optional, not present'}] {rel}  - {why}")

    if (ROOT / "models/best_supervised_model.pkl").exists():
        try:
            import joblib
            import pandas as pd

            model = joblib.load(ROOT / "models/best_supervised_model.pkl")
            X = pd.read_csv(ROOT / "data/processed/X_test.csv", nrows=5)
            proba = model.predict_proba(X)[:, 1]
            print(f"\nModel loaded: {type(model).__name__}; sample fraud probabilities: {proba.round(6).tolist()}")
        except Exception as exc:
            ok = False
            print(f"\n[FAIL] Could not load/use the model: {exc}\n"
                  "       Check that the installed lightgbm/scikit-learn versions match requirements-api.txt.")
    print("\nSetup OK." if ok else "\nSetup INCOMPLETE - see items marked MISSING / FAIL.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
