from abc import ABC, abstractmethod

from src.domain.identity import ListRepository
from .sale import Sale, SaleCollection


class SaleRepository(ListRepository[Sale], ABC):
    """
    Abstract base class for Sale repository.
    Defines the interface for obtaining Sale entities from a data store.
    """
    @abstractmethod
    async def obtain_by_number(self, number: str) -> Sale | None: ...

    @abstractmethod
    async def obtain_by_customer(self, customer_id: str, limit: int | None = None) -> SaleCollection: ...
