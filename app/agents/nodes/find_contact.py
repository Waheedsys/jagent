import httpx
from app.config import settings

APOLLO_SEARCH_URL = "https://api.apollo.io/api/v1/mixed_people/search"

async def find_contact_node(state: dict) -> dict:
    company_domain = state.get("company_domain") or guess_domain(state["company"])

    payload = {
        "api_key": settings.apollo_api_key,
        "q_organization_domains": company_domain,
        "person_titles": ["Technical Recruiter", "Talent Acquisition", "Recruiter", "Hiring Manager"],
        "page": 1,
        "per_page": 5,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(APOLLO_SEARCH_URL, json=payload)
        resp.raise_for_status()
        data = resp.json()

    people = data.get("people", [])
    if not people:
        state["recruiter_email"] = None
        state["recruiter_name"] = None
        return state

    # prefer someone with "technical" or "engineering" in title if present
    best = next(
        (p for p in people if "technical" in p.get("title", "").lower() or "engineer" in p.get("title", "").lower()),
        people[0],
    )

    state["recruiter_name"] = best.get("name")
    state["recruiter_email"] = best.get("email")  # may be null until "unlocked"
    state["recruiter_title"] = best.get("title")
    return state


def guess_domain(company_name: str) -> str:
    # naive fallback — replace with a proper company->domain lookup (e.g. Clearbit) if this misses often
    return company_name.lower().replace(" ", "") + ".com"