from src.domain.author import AuthorRepository
from src.domain.book import BookRepository, Book
from src.domain.book.exception import BookAlreadyExistsError
from src.domain.editorial import EditorialRepository
from src.domain.user import UserRepository
from .book_create_payload import BookCreatePayload
from .book_makeable import BookMakeable


class BookCreate(BookMakeable):
    """
    Use case for creating a book.

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

    async def dispatch(self, payload: BookCreatePayload) -> Book:
        """
        Create a new book based on the provided payload.

        :param payload: Data required to create a new book.
        :return: The created Book object.
        """
        await self._check_already_exists(payload)

        user = self.repo_user.obtain_user()
        author = await self._find_author(payload.author_id)
        editorial = await self._find_editorial(payload.editorial_id)
        detail = self._make_detail(payload.detail)
        sale = self._make_sale(payload.sale)

        book = Book.create(
            title=payload.title,
            description=payload.description,
            author=author,
            editorial=editorial,
            detail=detail,
            sale=sale,
            created_by=user.name,
        )

        await self.repo_book.save(book)
        return book

    async def _check_already_exists(self, payload):
        book = await self.repo_book.obtain_by_title(payload.title)
        if book is not None:
            raise BookAlreadyExistsError()
