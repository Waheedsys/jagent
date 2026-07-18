import httpx
from app.config import settings
from .base import ContactProvider, ContactResult

RELEVANT_DEPARTMENTS = {"hr", "recruiting", "human_resources"}
RELEVANT_TITLE_KEYWORDS = ["recruit", "talent", "people", "hr", "hiring", "engineering", "technical"]

class HunterProvider(ContactProvider):
    async def find_contact(self, company_domain: str, titles: list[str]) -> ContactResult | None:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://api.hunter.io/v2/domain-search",
                params={"domain": company_domain, "api_key": settings.hunter_api_key},
            )
            resp.raise_for_status()
            emails = resp.json()["data"].get("emails", [])
        
        print(f"Total emails found for {company_domain}: {len(emails)}")
        for e in emails:
            print(f"  {e.get('value')} — dept: {e.get('department')} — title: {e.get('position')}")

        if not emails:
            return None

        relevant = [
            e for e in emails
            if e.get("department") in RELEVANT_DEPARTMENTS
            or any(kw in (e.get("position") or "").lower() for kw in RELEVANT_TITLE_KEYWORDS)
        ]

        if not relevant:
            return None  # no hiring-relevant contact — don't fall back to a random department

        best = max(relevant, key=lambda e: e.get("confidence", 0))
        return ContactResult(
            name=f"{best.get('first_name','')} {best.get('last_name','')}".strip(),
            email=best.get("value"),
            title=best.get("position"),
            source="hunter",
        )

    async def credits_remaining(self) -> int | None:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://api.hunter.io/v2/account", params={"api_key": settings.hunter_api_key}
            )
            data = resp.json()["data"]
            return data["requests"]["searches"]["available"] - data["requests"]["searches"]["used"]