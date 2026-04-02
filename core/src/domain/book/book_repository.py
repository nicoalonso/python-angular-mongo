from abc import ABC, abstractmethod

from src.domain.book import Book, BookCollection
from src.domain.identity import ListRepository


class BookRepository(ListRepository[Book], ABC):
    """
    Abstract base class for Book repository.
    Defines the interface for obtaining Book entities from a data store.
    """
    @abstractmethod
    async def obtain_by_title(self, title: str) -> Book | None: ...

    @abstractmethod
    async def obtain_by_author(self, author_id: str, limit: int | None = None) -> BookCollection: ...

    @abstractmethod
    async def obtain_by_editorial(self, editorial_id: str, limit: int | None = None) -> BookCollection: ...
