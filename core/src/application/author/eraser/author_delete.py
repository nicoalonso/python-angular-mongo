from src.domain.author import AuthorRepository, Author
from src.domain.author.exception import AuthorNotFoundError
from src.domain.book import BookRepository
from .author_book_associated_error import AuthorBookAssociatedError


class AuthorDelete:
    """
    Use case for deleting an existing author.

    :ivar repo_author: Repository for author data access.
    """
    def __init__(
            self,
            repo_author: AuthorRepository,
            repo_book: BookRepository,
    ):
        self.repo_author = repo_author
        self.repo_book = repo_book

    async def dispatch(self, author_id: str) -> None:
        author = await self.repo_author.obtain_by_id(author_id)
        if not author:
            raise AuthorNotFoundError(author_id)

        await self._search_books_related(author)

        await self.repo_author.remove(author_id)

    async def _search_books_related(self, author: Author) -> None:
        books = await self.repo_book.obtain_by_author(author.id, 1)

        if not books.is_empty():
            raise AuthorBookAssociatedError(author.id)
