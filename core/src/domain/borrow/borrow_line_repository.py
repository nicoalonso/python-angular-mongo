from abc import ABC, abstractmethod

from src.domain.identity import ListRepository
from .borrow_line import BorrowLine, BorrowLineCollection


class BorrowLineRepository(ListRepository[BorrowLine], ABC):
    """
    Abstract base class for BorrowLine repository.
    Defines the interface for obtaining BorrowLine entities from a data store.
    """
    @abstractmethod
    async def obtain_by_borrow(self, borrow_id: str) -> BorrowLineCollection: ...

    @abstractmethod
    async def obtain_by_book(self, book_id: str, limit: int | None = None) -> BorrowLineCollection: ...

    @abstractmethod
    async def obtain_active_by_book(self, book_id: str) -> BorrowLineCollection: ...
