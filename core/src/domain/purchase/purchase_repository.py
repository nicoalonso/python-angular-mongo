from abc import ABC, abstractmethod

from src.domain.identity import ListRepository
from src.domain.purchase.purchase import Purchase, PurchaseCollection


class PurchaseRepository(ListRepository[Purchase], ABC):
    """
    Abstract base class for Purchase repository.
    Defines the interface for obtaining Purchase entities from a data store.
    """
    @abstractmethod
    async def obtain_by_provider_and_number(self, provider_id: str, invoice_number: str) -> Purchase | None: ...

    @abstractmethod
    async def obtain_by_provider(self, provider_id: str, limit: int | None = None) -> PurchaseCollection: ...
