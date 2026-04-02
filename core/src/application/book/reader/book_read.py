from src.domain.book import Book, BookRepository
from src.domain.book.exception import BookNotFoundError


class BookRead:
    """
    Use case for reading a book.
    """
    def __init__(self, repo_book: BookRepository):
        self.repo_book = repo_book

    async def dispatch(self, book_id: str) -> Book:
        book = await self.repo_book.obtain_by_id(book_id)
        if not book:
            raise BookNotFoundError(book_id)

        return book
