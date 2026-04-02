from abc import ABC

from src.application.book.creator.payload import BookDetailPayload, BookSalePayload
from src.domain.author import AuthorRepository, Author
from src.domain.author.exception import AuthorNotFoundError
from src.domain.book import BookDetail, BookSale
from src.domain.editorial import EditorialRepository, Editorial
from src.domain.editorial.exception import EditorialNotFoundError


class BookMakeable(ABC):
    """
    Abstract class for book creation.

    :ivar repo_author: Repository for author data access.
    :ivar repo_editorial: Repository for editorial data access.
    """
    def __init__(
            self,
            repo_author: AuthorRepository,
            repo_editorial: EditorialRepository,
    ):
        self.repo_author = repo_author
        self.repo_editorial = repo_editorial

    async def _find_author(self, author_id: str) -> Author:
        """
        Find an author by ID.
        :param author_id: The ID of the author to find.
        :return: The found author
        """
        author = await self.repo_author.obtain_by_id(author_id)
        if author is None:
            raise AuthorNotFoundError(author_id)

        return author

    async def _find_editorial(self, editorial_id: str) -> Editorial:
        """
        Find an editorial by ID.
        :param editorial_id: The ID of the editorial to find.
        :return: The found editorial
        """
        editorial = await self.repo_editorial.obtain_by_id(editorial_id)
        if editorial is None:
            raise EditorialNotFoundError(editorial_id)

        return editorial

    @staticmethod
    def _make_detail(payload: BookDetailPayload) -> BookDetail:
        """
        Create a BookDetail object from the given payload.
        :param payload: The payload containing the details of the book.
        :return: The created BookDetail object.
        """
        return BookDetail.create(
            edition=payload.edition,
            isbn=payload.isbn,
            language=payload.language,
            published_at=payload.published_at,
            pages=payload.pages,
        )

    @staticmethod
    def _make_sale(payload: BookSalePayload) -> BookSale:
        """
        Create a BookSale object from the given payload.
        :param payload: The payload containing the sale details of the book.
        :return: The created BookSale object.
        """
        return BookSale(
            saleable=payload.saleable,
            price=payload.price,
            discount=payload.discount,
        )
