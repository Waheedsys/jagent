import httpx
from app.config import settings
from .base import ContactProvider, ContactResult

class ApolloProvider(ContactProvider):
    async def find_contact(self, company_domain: str, titles: list[str]) -> ContactResult | None:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.apollo.io/api/v1/mixed_people/search",
                json={
                    "api_key": settings.apollo_api_key,
                    "q_organization_domains": company_domain,
                    "person_titles": titles,
                    "per_page": 5,
                },
            )
            resp.raise_for_status()
            people = resp.json().get("people", [])
            if not people:
                return None
            best = people[0]
            return ContactResult(
                name=best.get("name"), email=best.get("email"), title=best.get("title"), source="apollo"
            )

    async def credits_remaining(self) -> int | None:
        return None  # Apollo doesn't expose this cleanly via API; track manually or catch 402/429