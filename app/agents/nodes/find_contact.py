import httpx
from app.config import settings
from app.core.contact_providers.router import ContactFinderRouter

APOLLO_SEARCH_URL = "https://api.apollo.io/api/v1/mixed_people/search"

router = ContactFinderRouter()

async def find_contact_node(state: dict) -> dict:
    domain=state.get("company_domain") or guess_domain(state["company"])
    result = await router.find_contact(
        company_domain=domain,
        titles=["Technical Recruiter", "Talent Acquisition", "Recruiter"],
    )
    if result:
        state["recruiter_name"] = result.name
        state["recruiter_email"] = result.email
        state["contact_source"] = result.source
    else:
        state["recruiter_email"] = None
    return state

def guess_domain(company_name: str) -> str:
    # naive fallback — replace with a proper company->domain lookup (e.g. Clearbit) if this misses often
    return company_name.lower().replace(" ", "") + ".com"