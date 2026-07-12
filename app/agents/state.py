from typing_extensions import TypedDict, Optional

class OutreachState(TypedDict):
    company: str
    role_title: str
    job_description: str
    resume_summary: str
    fit_score: Optional[float]
    recruiter_name: Optional[str]
    recruiter_email: Optional[str]
    draft_email: Optional[str]
    draft_subject: Optional[str]
    human_feedback: Optional[str]
    revision_count: int
    approved: bool
    company_domain: Optional[str]