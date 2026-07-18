from app.core.llm_client import call_llm
from app.config import settings

DRAFT_PROMPT = """You are drafting a cold email from {candidate_name}, a candidate, to a recruiter about a role.

Candidate background (use only what's relevant to THIS role):
{resume_summary}

Company: {company}
Role: {role_title}
Job description:
{job_description}

Recruiter name (if known): {recruiter_name}

Revision feedback (if any, apply this): {human_feedback}

Rules:
- CRITICAL: Only reference facts, technologies, and claims explicitly present in the
  candidate background above. Do NOT invent metrics (%, latency, uptime, query volume),
  tools, or outcomes that aren't stated. If the background doesn't give you a concrete
  number, don't manufacture one — describe the work qualitatively instead.
- 120-150 words max, strictly. Recruiters skim.
- Open with ONE specific, concrete hook tying the candidate's actual work to something in the job description.
  Do NOT open with "I'm passionate about..." or "I came across this role..."
- No buzzwords: "passionate", "excited to leverage", "dynamic", "synergy", "detail-oriented"
- End with a clear, low-friction ask (e.g. "open to a quick 15-min call this week?")
- Sign off with just the first name: {candidate_name}
- Write like a competent engineer emailing a peer, not a formal cover letter

Return ONLY the email body, no subject line, no preamble, no markdown.
"""

SUBJECT_PROMPT = """Write a short, specific email subject line (under 8 words) for a cold email
about the {role_title} role at {company}.

The email body already opens with this concrete hook — the subject should echo the
same specific technical detail, not restate the role title:
{email_body}

Rules:
- No buzzwords: "passionate", "excited", "dynamic", "power", "future", "unlock", "transform"
- No hype or grandiose framing (e.g. "Power X's AI Future")
- No "Application for..." or generic phrasing
- Should read like a peer referencing shared technical ground, not a marketing headline
- Reference a specific technology or concept from the hook, not just the role/company name

Return only the subject line, nothing else.
"""

async def draft_email_node(state: dict) -> dict:
    if not state.get("recruiter_email"):
        state["draft_email"] = None
        return state

    body = await call_llm(
        DRAFT_PROMPT.format(
             candidate_name=settings.candidate_name,
            resume_summary=state["resume_summary"],
            company=state["company"],
            role_title=state["role_title"],
            job_description=state["job_description"],
            recruiter_name=state.get("recruiter_name") or "there",
            human_feedback=state.get("human_feedback") or "None — first draft",
        )
    )

    subject = await call_llm(
        SUBJECT_PROMPT.format(role_title=state["role_title"], company=state["company"], email_body=body.strip(),)
    )
    
    body = body.strip()

    if not body.endswith(settings.candidate_name):
        body = f"{body}\n\n{settings.candidate_name}"

    state["draft_email"] = body.strip()
    state["draft_subject"] = subject.strip()
    state["revision_count"] = state.get("revision_count", 0) + 1
    return state