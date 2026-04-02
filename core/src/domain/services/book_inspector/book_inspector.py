from abc import ABC, abstractmethod

from src.domain.book import Book
from src.domain.borrow import BorrowLineRepository, BorrowLineCollection


class BookInspector(ABC):
    """
    Abstract base class for book inspectors. Defines the interface for inspecting books.
    """
    def __init__(self, repo_borrow_line: BorrowLineRepository):
        self.repo_borrow_line = repo_borrow_line

    @abstractmethod
    async def available(self, book: Book) -> bool: ...

    async def _obtain_active_borrows(self, book: Book) -> BorrowLineCollection:
        """
        Obtain active borrows for a given book.
        :param book: The book to check for active borrows.
        :return: A list of active borrows for the given book.
        """
        return await self.repo_borrow_line.obtain_active_by_book(book.id)
