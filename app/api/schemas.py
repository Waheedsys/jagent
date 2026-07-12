from pydantic import BaseModel
from typing import Optional

class ScoreRequest(BaseModel):
    company: str
    role_title: str
    job_description: str
    resume_summary: str
    fit_score: Optional[float] = None