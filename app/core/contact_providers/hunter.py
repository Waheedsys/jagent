import httpx
from app.config import settings
from .base import ContactProvider, ContactResult

class HunterProvider(ContactProvider):
    async def find_contact(self, company_domain: str, titles: list[str]) -> ContactResult | None:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://api.hunter.io/v2/domain-search",
                params={"domain": company_domain, "api_key": settings.hunter_api_key, "department": "hr"},
            )
            resp.raise_for_status()
            data = resp.json()["data"]
            emails = data.get("emails", [])
            if not emails:
                return None
            best = max(emails, key=lambda e: e.get("confidence", 0))
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