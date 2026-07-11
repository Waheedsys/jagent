from typing_extensions import TypedDict, Optional

class OutreachState(TypedDict):
    company: str
    role_title: str
    job_description: str
    resume_summary: str
    fit_score: Optional[float]