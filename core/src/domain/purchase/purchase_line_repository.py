from abc import ABC, abstractmethod

from src.domain.identity import ListRepository
from src.domain.purchase.purchase_line import PurchaseLine, PurchaseLineCollection


class PurchaseLineRepository(ListRepository[PurchaseLine], ABC):
    """
    Abstract base class for PurchaseLine repository.
    Defines the interface for obtaining PurchaseLine entities from a data store.
    """
    @abstractmethod
    async def obtain_by_purchase(self, purchase_id: str) -> PurchaseLineCollection: ...

    @abstractmethod
    async def obtain_by_book(self, book_id: str, limit: int | None = None) -> PurchaseLineCollection: ...
