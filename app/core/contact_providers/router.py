from .hunter import HunterProvider
from .apollo import ApolloProvider
from .base import ContactResult
import httpx

class ContactFinderRouter:
    def __init__(self):
        self.providers = [HunterProvider(), ApolloProvider()]  # order = preference

    async def find_contact(self, company_domain: str, titles: list[str]) -> ContactResult | None:
        for provider in self.providers:
            try:
                result = await provider.find_contact(company_domain, titles)
                if result and result.email:
                    return result
            except httpx.HTTPStatusError as e:
                if e.response.status_code in (402, 403, 429):
                    # credits exhausted or rate-limited — log and fall through to next provider
                    continue
                raise
        return None