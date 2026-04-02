from src.domain.author import AuthorRepository
from src.domain.book import BookRepository, Book
from src.domain.book.exception import BookNotFoundError
from src.domain.editorial import EditorialRepository
from src.domain.user import UserRepository
from src.application.book.creator import BookMakeable
from .book_update_payload import BookUpdatePayload


class BookUpdate(BookMakeable):
    """
    Use case for updating a book.

    :ivar repo_book: Repository for book data access.
    :ivar repo_user: Repository for user data access.
    """
    def __init__(
            self,
            repo_book: BookRepository,
            repo_author: AuthorRepository,
            repo_editorial: EditorialRepository,
            repo_user: UserRepository,
    ):
        super().__init__(repo_author, repo_editorial)

        self.repo_book = repo_book
        self.repo_user = repo_user

    async def dispatch(self, book_id: str, payload: BookUpdatePayload) -> Book:
        """
        Update an existing book based on the provided book ID and payload.

        :param book_id: The ID of the book to be updated.
        :param payload: (BookUpdatePayload) Data required to update the book.
        :return: The updated Book object.
        """
        book = await self.find_book_or_fail(book_id)

        author = await self._find_author(payload.author_id)
        editorial = await self._find_editorial(payload.editorial_id)
        detail = self._make_detail(payload.detail)
        sale = self._make_sale(payload.sale)
        user = self.repo_user.obtain_user()

        book.modify(
            title=payload.title,
            description=payload.description,
            author=author,
            editorial=editorial,
            detail=detail,
            sale=sale,
            updated_by=user.name,
        )
        await self.repo_book.save(book)

        return book

    async def find_book_or_fail(self, book_id: str) -> Book:
        """
        Find a book by its ID or raise an error if it does not exist.

        :param book_id: The ID of the book to find.
        :return: The found Book object.
        """
        book = await self.repo_book.obtain_by_id(book_id)
        if book is None:
            raise BookNotFoundError(book_id)

        return book
