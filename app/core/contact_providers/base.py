from abc import ABC, abstractmethod
from typing import Optional
from pydantic import BaseModel

class ContactResult(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    title: Optional[str] = None
    source: str  # "hunter" | "apollo"

class ContactProvider(ABC):
    @abstractmethod
    async def find_contact(self, company_domain: str, titles: list[str]) -> Optional[ContactResult]:
        ...

    @abstractmethod
    async def credits_remaining(self) -> Optional[int]:
        """Return None if the provider doesn't expose this."""
        ...