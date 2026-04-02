from src.domain.book import BookRepository
from src.domain.editorial import EditorialRepository, Editorial
from src.domain.editorial.exception import EditorialNotFoundError
from .editorial_book_associated_error import EditorialBookAssociatedError


class EditorialDelete:
    """
    Use case for deleting an existing editorial.

    :ivar repo_editorial: Repository for editorial data access.
    """
    def __init__(
            self,
            repo_editorial: EditorialRepository,
            repo_book: BookRepository,
    ):
        self.repo_editorial = repo_editorial
        self.repo_book = repo_book

    async def dispatch(self, editorial_id: str) -> None:
        """Delete an existing editorial by its ID."""
        editorial = await self.repo_editorial.obtain_by_id(editorial_id)
        if not editorial:
            raise EditorialNotFoundError(editorial_id)

        await self._search_books_related(editorial)

        await self.repo_editorial.remove(editorial_id)

    async def _search_books_related(self, editorial: Editorial) -> None:
        """
        Search for books related to the given editorial and raise an exception if any are found.
        :param editorial:
        :return:
        """
        books = await self.repo_book.obtain_by_editorial(editorial.id, 1)
        if not books.is_empty():
            raise EditorialBookAssociatedError(editorial.id)
