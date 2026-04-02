from abc import ABC, abstractmethod

from src.domain.identity import ListRepository
from .sale_line import SaleLine, SaleLineCollection


class SaleLineRepository(ListRepository[SaleLine], ABC):
    """
    Abstract base class for SaleLine repository.
    Defines the interface for obtaining SaleLine entities from a data store.
    """
    @abstractmethod
    async def obtain_by_sale(self, sale_id: str) -> SaleLineCollection: ...

    @abstractmethod
    async def obtain_by_book(self, book_id: str, limit: int | None = None) -> SaleLineCollection: ...
