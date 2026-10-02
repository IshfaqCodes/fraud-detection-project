# Free Online Deployment Guide (step by step)

Goal: get a public link anyone (e.g. Hassan) can open in a browser, without installing anything.

| Part | Where (free) | Result |
|------|--------------|--------|
| Dashboard (main demo) | Streamlit Community Cloud | `https://<name>.streamlit.app` |
| API (`/predict`, Swagger docs) | Render (free web service) | `https://<name>.onrender.com/docs` |

The dashboard loads the model by itself (it does not call the API), so **Part 2 alone is already a
complete, working demo**. Part 3 adds the live API.

Free-tier limits change over time, so check the current limits on each site's pricing page.

---

## Part 1: Put the project on GitHub

1. Create a free account at https://github.com and click **New repository**.
   Name it `fraud-detection-project`, set it to **Public** (Streamlit's free tier works best with public repos), do **not** add a README (you already have one).
2. Make sure the big files are NOT committed. `.gitignore` already excludes `data/creditcard.csv` and
   `data/processed/X_train.csv` (GitHub rejects files over 100 MB).
3. Make sure these files ARE present in the folder (the app needs them):
   - `models/best_supervised_model.pkl`, `models/risk_scoring_config.pkl`, `models/scaler_params.json`, `models/shap_feature_importance.csv`
   - `data/processed/X_test.csv`, `data/processed/y_test.csv`
4. Open a terminal in the project folder and run:

```bash
git init
git add .
git commit -m "Fraud detection project"
git branch -M main
git remote add origin https://github.com/<your-username>/fraud-detection-project.git
git push -u origin main
```

5. Refresh the GitHub page and confirm the `models/` and `data/processed/` files are there.

> If `git push` says a file is too large, run `git rm --cached <that file>`, add it to `.gitignore`, commit and push again.

---

## Part 2: Dashboard on Streamlit Community Cloud

1. Go to https://share.streamlit.io and sign in with GitHub. Allow access to your repository.
2. Click **Create app** (or **New app**) and choose **Deploy a public app from GitHub**.
3. Fill in:
   - Repository: `<your-username>/fraud-detection-project`
   - Branch: `main`
   - Main file path: `src/dashboard.py`
4. Click **Advanced settings** and set **Python version = 3.12** (the pinned packages need Python 3.11+, and the default may be older).
   Note: a `runtime.txt` file does not work here; the version must be chosen in this dialog.
5. Click **Deploy** and wait a few minutes while it installs `requirements.txt`.
6. Your app opens at `https://<something>.streamlit.app`. You can change the subdomain in the app settings.
7. Test: click **Open dashboard** on the welcome screen, then open the **Score a transaction** tab,
   click **Load random fraud** and check that the band is High and the SHAP chart appears.

Common problems:

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | A package is missing from `requirements.txt`; add it, commit, push (the app redeploys itself) |
| Install fails on pandas/numpy | Python version is too old; change it to 3.12 in app settings, then reboot |
| "Missing model files" | The `.pkl` / `.json` files were not pushed; check `git status` and push them |
| App sleeps after inactivity | Normal on the free tier; opening the link wakes it up (takes ~30 seconds) |

---

## Part 3: API on Render (optional, for the live `/docs` page)

1. Go to https://render.com and sign up with GitHub.
2. Click **New +** -> **Web Service** -> connect your `fraud-detection-project` repository.
3. Fill in:
   - Language / Runtime: **Docker**
   - Dockerfile Path: `./Dockerfile.api`
   - Instance type: **Free**
   - Advanced -> Health Check Path: `/health`
4. Click **Create Web Service** and wait for the build (several minutes the first time).
5. If the log says no open port was detected, add an environment variable `PORT` = `8000` and redeploy.
6. Open `https://<your-service>.onrender.com/docs`, expand `POST /predict`, click **Try it out**
   (the example transaction is pre-filled) and click **Execute**. You should get a fraud probability,
   a risk score, a risk band and the top 5 SHAP factors.
7. Quick check from a terminal: `curl https://<your-service>.onrender.com/health`

Notes:
- The free instance goes to sleep when idle, so the first request after a pause can take about a minute. Open the link a minute before showing it to someone.
- The free tier has limited memory (512 MB at the time of writing). LightGBM + SHAP is fairly light, but if the service crashes with an out-of-memory error, use Hugging Face Spaces (below) instead.

---

## Alternative: Hugging Face Spaces (free, more memory)

Good if Render runs out of memory, or if you want one place for everything.

1. Create an account at https://huggingface.co and click **New** -> **Space**.
2. Choose **Docker** as the SDK, a blank template, and **Public**.
3. In the Space, you need a file named exactly `Dockerfile` and a `README.md` starting with:

```yaml
---
title: Fraud Detection API
sdk: docker
app_port: 7860
---
```

4. Copy the contents of `Dockerfile.api` into `Dockerfile` and change the last line to use port 7860:
   `CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]`
   (also change `EXPOSE 8000` to `EXPOSE 7860`).
5. Upload the `src/` and `models/` folders (the three model files plus `requirements-api.txt`) to the Space and let it build.
6. The API is then at `https://<username>-<space-name>.hf.space/docs`.

---

## What to send Hassan

- Dashboard link: `https://<name>.streamlit.app`
- API docs link: `https://<name>.onrender.com/docs`
- GitHub repository link (he can clone it and follow `README.md`)
- A note that the free services sleep when idle, so the first load can take up to a minute.

## Security note

These public demo links have no login. The demo uses the public credit-card dataset (anonymized), so it is
fine to share. Do not put real customer data into it.
