from app.core.embeddings import embed_text
import numpy as np

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

async def score_fit_node(state: dict) -> dict:
    jd_vec = embed_text(state["job_description"])
    resume_vec = embed_text(state["resume_summary"])
    state["fit_score"] = float(cosine_sim(jd_vec, resume_vec))
    return state