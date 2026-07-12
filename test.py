# test_hunter_multi.py
import asyncio
from app.core.contact_providers.hunter import HunterProvider

TEST_DOMAINS = [
    "google.com",
]

async def test():
    provider = HunterProvider()
    for domain in TEST_DOMAINS:
        print(f"\n--- {domain} ---")
        try:
            result = await provider.find_contact(domain, titles=[])
            print(result)
        except Exception as e:
            print(f"Error: {e}")

asyncio.run(test())