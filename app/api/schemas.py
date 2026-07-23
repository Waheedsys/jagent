from pydantic import BaseModel
from typing import Optional
from app.agents.nodes.score_fit.score_schema import FitEvaluation
class ScoreRequest(BaseModel):
    company: str
    role_title: str
    job_description: str
    resume_summary: str
    fit_evaluation: Optional[FitEvaluation] = None 
    company_domain: Optional[str] = None