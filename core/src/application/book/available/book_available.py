from src.domain.book import BookRepository
from src.domain.book.exception import BookNotFoundError
from src.domain.services.book_inspector import BookInspectFactory


class BookAvailable:
    """
    Use case for checking if a book is available for borrowing or sale.

    :ivar repo_book: Repository for accessing book data.
    :ivar factory: Factory for creating book inspection services.
    """
    def __init__(
            self,
            repo_book: BookRepository,
            factory: BookInspectFactory,
    ):
        self.repo_book = repo_book
        self.factory = factory

    async def dispatch(self, book_id: str, is_sale: bool) -> bool:
        """
        Check if the book with the given ID is available.

        :param book_id: The ID of the book to check.
        :param is_sale: Whether to check availability for sale (True) or borrowing (False).
        :return: True if the book is available, False otherwise.
        """
        book = await self.repo_book.obtain_by_id(book_id)
        if not book:
            raise BookNotFoundError(book_id)

        inspector = self.factory.create(is_sale)
        return await inspector.available(book)
