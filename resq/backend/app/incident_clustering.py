"""Incident clustering: cosine similarity of TF-IDF vectors + agglomerative clustering."""
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def cluster(texts, threshold=0.45):
    X = TfidfVectorizer(stop_words="english").fit_transform(texts)
    d = 1 - cosine_similarity(X)
    lab = AgglomerativeClustering(n_clusters=None, metric="precomputed", linkage="average", distance_threshold=threshold).fit_predict(d)
    out = {}
    for t, l in zip(texts, lab): out.setdefault(int(l), []).append(t)
    return [{"id": i + 1, "reports": len(v), "samples": v[:3]} for i, v in enumerate(sorted(out.values(), key=len, reverse=True))]

DEMO = [{"id":1,"name":"Ridgeview Wildfire","urgency":"HIGH","reports":14,"terms":["wildfire","evacuation","hills"],"lat":34,"lon":-118},
        {"id":2,"name":"Storm Power Outage","urgency":"MEDIUM","reports":8,"terms":["power lines","storm","block"],"lat":41,"lon":-87},
        {"id":3,"name":"Minor Earthquake","urgency":"LOW","reports":6,"terms":["earthquake","3.2","shaken"],"lat":36,"lon":140}]
