# app/core/contact_providers/prospeo.py
import httpx
from app.config import settings
from .base import ContactProvider, ContactResult

PROSPEO_BASE_URL = "https://api.prospeo.io"

# error_codes that mean "legitimately nothing found" rather than "something's broken"
BENIGN_ERROR_CODES = {"NO_RESULTS"}


class ProspeoProvider(ContactProvider):
    async def _post(self, client: httpx.AsyncClient, path: str, payload: dict) -> dict | None:
        """POST to Prospeo, returning None for benign zero-match errors,
        raising for anything else (so the router's 402/403/429 fallback still works)."""
        resp = await client.post(
            f"{PROSPEO_BASE_URL}{path}",
            headers=self._headers(),
            json=payload,
        )
        if resp.status_code == 400:
            body = resp.json()
            if body.get("error_code") in BENIGN_ERROR_CODES:
                return None
            resp.raise_for_status()  # real 400 (bad filters, bad payload) — surface it

        resp.raise_for_status()  # 402/403/429/5xx — propagates to router
        data = resp.json()
        return None if data.get("error") else data

    async def find_contact(self, company_domain: str, titles: list[str]) -> ContactResult | None:
        async with httpx.AsyncClient() as client:
            candidate = await self._search_person(client, company_domain, titles)
            if not candidate:
                return None
            return await self._enrich_person(client, candidate, company_domain)

    async def _search_person(
        self, client: httpx.AsyncClient, company_domain: str, titles: list[str]
    ) -> dict | None:
        filters: dict = {"company": {"websites": {"include": [company_domain]}}}
        if titles:
            filters["person_job_title"] = {"include": titles}

        data = await self._post(client, "/search-person", {"page": 1, "filters": filters})
        if not data:
            return None

        results = data.get("results", [])
        print(f"Total candidates found for {company_domain}: {len(results)}")
        for r in results:
            p = r.get("person", {})
            print(f"  {p.get('full_name')} — title: {p.get('current_job_title')}")

        return results[0]["person"] if results else None

    async def _enrich_person(
        self, client: httpx.AsyncClient, candidate: dict, company_domain: str
    ) -> ContactResult | None:
        data = await self._post(
            client,
            "/enrich-person",
            {
                "only_verified_email": True,
                "data": {
                    "person_id": candidate.get("person_id"),
                    "first_name": candidate.get("first_name"),
                    "last_name": candidate.get("last_name"),
                    "company_website": company_domain,
                },
            },
        )
        if not data:
            return None  # matched a candidate but no VERIFIED email — clean miss

        person = data.get("person", {})
        email_info = person.get("email", {})
        if not email_info.get("email"):
            return None

        return ContactResult(
            name=person.get("full_name") or f"{person.get('first_name','')} {person.get('last_name','')}".strip(),
            email=email_info["email"],
            title=person.get("current_job_title"),
            source="prospeo",
        )

    async def credits_remaining(self) -> int | None:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{PROSPEO_BASE_URL}/account-information", headers=self._headers())
            resp.raise_for_status()
            return resp.json().get("remaining_credits")

    def _headers(self) -> dict:
        return {"X-KEY": settings.prospeo_api_key, "Content-Type": "application/json"}