# test_prospeo_multi.py
import asyncio
from app.core.contact_providers.prospeo import ProspeoProvider

TEST_TITLES = ["recruiter", "talent", "technical recruiter"]


async def run_case(provider: ProspeoProvider, domain: str, titles: list[str], label: str):
    print(f"\n--- {label}: {domain} | titles={titles or 'NONE'} ---")
    try:
        result = await provider.find_contact(domain, titles=titles)
        print(result if result else "No match (clean NO_RESULTS, not an error)")
    except Exception as e:
        print(f"Real error: {e}")


async def test():
    provider = ProspeoProvider()

    remaining = await provider.credits_remaining()
    print(f"Prospeo credits remaining: {remaining}")

    # Case 1: domain only, no title filter — isolates whether Google has ANY
    # matchable people in Prospeo's DB at all
    await run_case(provider, "google.com", [], "domain-only")

    # Case 2: domain + your original recruiter titles
    await run_case(provider, "google.com", TEST_TITLES, "domain+titles")

    # Case 3: same titles, smaller/different company — rules out Google-specific
    # data restrictions vs. a filter/payload problem
    await run_case(provider, "stripe.com", TEST_TITLES, "control-company")


asyncio.run(test())