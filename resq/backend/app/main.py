from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from . import incident_clustering as clustering, explainability as ex

app = FastAPI(title="ResQ API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
class Report(BaseModel): text: str

@app.post("/api/analyze")
def analyze(r: Report):
    return ex.analyze(r.text)
@app.post("/api/explain")
def explain(r: Report): return ex.explain(r.text)
@app.get("/api/incidents")
def incidents(threshold: float = 0.45): return {"demo": True, "threshold": threshold, "incidents": clustering.DEMO}
@app.get("/api/analytics")
def analytics(range: str = "24h"):
    return {"demo": True, "range": range, "totals": {"reports":1284,"disasters":438,"high":87,"incidents":12}, "metrics": {"accuracy":.946,"precision":.941,"recall":.932,"f1":.936}}
@app.get("/api/model-info")
def info():
    return {"demo": ex.DEMO, "models": ["Naive Bayes","Logistic Regression","SVM"], "features": "TF-IDF", "explainability": "coef x TF-IDF row"}
@app.get("/api/health")
def health(): return {"status": "ok", "model_loaded": not ex.DEMO}
