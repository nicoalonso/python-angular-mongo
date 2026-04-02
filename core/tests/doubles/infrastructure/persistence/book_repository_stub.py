from typing import Optional

from src.domain.book import Book, BookCollection, BookRepository
from tests.fixtures import Ref
from tests.fixtures.mothers import BookMother
from .entity_repository_stub import EntityRepositoryStub
from .author_repository_stub import AuthorRepositoryStub
from .editorial_repository_stub import EditorialRepositoryStub


class BookRepositoryStub(EntityRepositoryStub[Book], BookRepository):
    """
    A stub for the BookRepository interface used in tests.

    :ivar repo_author: Optional[AuthorRepositoryStub] - An optional reference to an AuthorRepositoryStub for resolving author-related queries.
    :ivar repo_editorial: Optional[EditorialRepositoryStub] - An optional reference to an EditorialRepositoryStub for resolving editorial-related queries.
    """
    def __init__(
            self,
            *,
            repo_author: Optional[AuthorRepositoryStub] = None,
            repo_editorial: Optional[EditorialRepositoryStub] = None,
    ):
        self.repo_author: Optional[AuthorRepositoryStub] = repo_author
        self.repo_editorial: Optional[EditorialRepositoryStub] = repo_editorial

        super().__init__()

    async def obtain_by_title(self, title: str) -> Book | None:
        self.query_filter = title
        self._throw_error()
        return self.read

    async def obtain_by_author(self, author_id: str, limit: int | None = None) -> BookCollection:
        self.query_filter = author_id
        return self.list

    async def obtain_by_editorial(self, editorial_id: str, limit: int | None = None) -> BookCollection:
        self.query_filter = editorial_id
        return self.list

    def make_fixtures(self) -> None:
        shakespeare = None
        cervantes = None
        anaya = None

        if self.repo_author:
            shakespeare = self.repo_author.get(Ref.AuthorShakespeare)
            cervantes = self.repo_author.get(Ref.AuthorCervantes)

        if self.repo_editorial:
            anaya = self.repo_editorial.get(Ref.EditorialAnaya)

        romeo_and_juliet = BookMother.romeo_and_juliet(author=shakespeare, editorial=anaya)
        self.add_fixture(Ref.BookRomeoAndJuliet, romeo_and_juliet)

        don_quixote = BookMother.don_quijote(author=cervantes, editorial=anaya)
        self.add_fixture(Ref.BookDonQuijote, don_quixote)
