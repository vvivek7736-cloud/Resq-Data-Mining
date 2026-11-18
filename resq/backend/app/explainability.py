"""Explainable AI + classifier. Uses models/vectorizer.pkl & classifier.pkl if present, else DEMO mode."""
import math, os, re, joblib
LEX = {"trapped":2.41,"flooding":2.13,"rescue":1.87,"wildfire":2.2,"evacuation":1.9,"fire":1.8,"earthquake":1.9,
       "collapse":1.7,"rising":1.22,"emergency":.96,"asap":.71,"orders":.8,"water":.52,"hills":.4,"storm":.6,
       "lol":-.94,"love":-.71,"movie":-.55,"party":-.5}
M = os.path.join(os.path.dirname(__file__), "..", "..", "models")
try: VEC, CLF = joblib.load(f"{M}/vectorizer.pkl"), joblib.load(f"{M}/classifier.pkl")
except Exception: VEC = CLF = None
DEMO = VEC is None
sig = lambda x: 1 / (1 + math.exp(-x))

def contributions(text):
    if DEMO:
        return {w: LEX[w] for w in re.findall(r"[a-z0-9']+", text.lower()) if w in LEX}
    c = VEC.transform([text]).multiply(CLF.coef_[0]).toarray()[0]   # coef x TF-IDF row
    names = VEC.get_feature_names_out()
    return {names[i]: float(c[i]) for i in c.nonzero()[0]}

def explain(text, k=7):
    c = contributions(text)
    pos = sorted(((w, v) for w, v in c.items() if v > 0), key=lambda x: -x[1])[:k]
    neg = sorted(((w, v) for w, v in c.items() if v < 0), key=lambda x: x[1])[:3]
    return {"positive": pos, "negative": neg, "demo": DEMO}

def analyze(text):
    c = contributions(text)
    if DEMO: p = sig(sum(c.values()) * .9 - .4)
    elif hasattr(CLF, "predict_proba"): p = CLF.predict_proba(VEC.transform([text]))[0][1]
    else: p = sig(float(CLF.decision_function(VEC.transform([text]))[0]))
    d = p >= .5; conf = min(.985, p if d else 1 - p)
    kw = [w for w, _ in sorted(c.items(), key=lambda x: -x[1]) if c[w] > 0][:4]
    hi = bool(re.search(r"trapped|evacuat|rescue|collapse", text, re.I))
    urg = "LOW" if not d else ("HIGH" if hi or conf > .93 else "MEDIUM")
    return {"prediction": "DISASTER" if d else "NOT DISASTER", "confidence": round(conf, 3),
            "urgency": urg, "keywords": kw, "incident_id": None, "demo": DEMO}
