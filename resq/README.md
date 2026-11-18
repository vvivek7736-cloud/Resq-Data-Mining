# ResQ – AI-Powered Disaster Tweet Classification, Urgency Prioritization & Incident Intelligence

Pipeline: Tweet → Preprocess → TF-IDF → ML model (NB / LR / SVM) → Urgency → Explainable AI → Incident clustering → Dashboard.
No new ML models are needed for the new features (explain, clustering); they plug into the existing trained pipeline.

## Structure
- `frontend/index.html` – self-contained dashboard (intro, 3D globe, 4-stage scroll, feed, models). Runs with a built-in mock classifier ("DEMO MODE").
- `frontend/logo.svg` – ResQ logo.
- `backend/app/` – FastAPI: `main.py` (API routes), `explainability.py` (classifier + explainable AI), `incident_clustering.py` (incident grouping).
- `models/` – put `vectorizer.pkl` and `classifier.pkl` here (joblib, scikit-learn). Without them the API runs in demo mode.

## Run
Frontend: open `frontend/index.html`, or `cd frontend && python -m http.server 5173`.

Backend:
```
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Docs: http://localhost:8000/docs

## Endpoints
POST /api/analyze · POST /api/explain · GET /api/incidents?threshold= · GET /api/analytics · GET /api/model-info · GET /api/health

## Connecting the frontend
In `index.html`, the function `analyze(t)` is the mock classifier. Replace it with `fetch('http://localhost:8000/api/analyze', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({text:t})})` and map `prediction/confidence/urgency/keywords` to the `res` object.

## Notes
Linear models only (NB, LR, SVM) are explainable this way; an LSTM would remain a black box. Metrics shown in the demo UI are illustrative.
