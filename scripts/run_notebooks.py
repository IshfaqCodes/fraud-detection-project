"""Execute notebooks 06-10 top to bottom, in order, and save the outputs inside each notebook.

Run from the project root:  python scripts/run_notebooks.py
Options:  python scripts/run_notebooks.py 06 08     (run only some notebooks)

Order matters: 06 creates threshold_config.pkl, which 07, 08 and 09 read; 08 creates
risk_scoring_config.pkl, which the API and dashboard read.
"""
import sys
from pathlib import Path

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = [
    "06_evaluation_and_threshold",
    "07_explainability_shap",
    "08_risk_scoring",
    "09_mlflow_tracking",
    "10_model_monitoring",
]


def main(selected):
    todo = [n for n in NOTEBOOKS if not selected or any(n.startswith(s) for s in selected)]
    for name in todo:
        path = ROOT / "notebooks" / f"{name}.ipynb"
        print(f"Running {path.name} ...", flush=True)
        nb = nbformat.read(path, as_version=4)
        # cwd = notebooks/ because the notebooks use relative paths like ../models/
        NotebookClient(nb, timeout=1800, kernel_name="python3",
                       resources={"metadata": {"path": str(path.parent)}}).execute()
        nbformat.write(nb, path)
        print(f"  OK  {path.name}", flush=True)
    print("All requested notebooks ran without errors.")


if __name__ == "__main__":
    main(sys.argv[1:])
