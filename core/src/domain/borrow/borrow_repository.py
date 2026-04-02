from abc import ABC, abstractmethod

from src.domain.borrow.borrow import Borrow, BorrowCollection
from src.domain.identity import ListRepository


class BorrowRepository(ListRepository[Borrow], ABC):
    """
    Abstract base class for Borrow repository.
    Defines the interface for obtaining Borrow entities from a data store.
    """
    @abstractmethod
    async def obtain_by_number(self, number: str) -> Borrow | None: ...

    @abstractmethod
    async def obtain_by_customer(self, customer_id: str, limit: int | None = None) -> BorrowCollection: ...

    @abstractmethod
    async def obtain_by_overdue(self) -> BorrowCollection: ...
