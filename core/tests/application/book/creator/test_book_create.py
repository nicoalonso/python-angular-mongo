import pytest

from src.application.book.creator import BookCreate, BookCreatePayload
from src.domain.author.exception import AuthorNotFoundError
from src.domain.book.exception import BookAlreadyExistsError
from src.domain.editorial.exception import EditorialNotFoundError
from tests.doubles.infrastructure.persistence import BookRepositoryStub, AuthorRepositoryStub, EditorialRepositoryStub, \
    UserRepositoryStub
from tests.fixtures import FixturePayload, Ref


class TestBookCreate:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_author = AuthorRepositoryStub()
        self.repo_editorial = EditorialRepositoryStub()
        self.repo_book = BookRepositoryStub(
            repo_author=self.repo_author,
            repo_editorial=self.repo_editorial,
        )
        repo_user = UserRepositoryStub()
        self.creator = BookCreate(
            repo_book=self.repo_book,
            repo_author=self.repo_author,
            repo_editorial=self.repo_editorial,
            repo_user=repo_user,
        )

        self.loader = FixturePayload()

    @pytest.mark.asyncio
    async def test_should_fail_when_already_exists(self):
        self.repo_book.put(Ref.BookRomeoAndJuliet)

        data = self.loader.load('book')
        payload = BookCreatePayload(**data)

        with pytest.raises(BookAlreadyExistsError):
            await self.creator.dispatch(payload)

    @pytest.mark.asyncio
    async def test_should_fail_when_author_not_found(self):
        data = self.loader.load('book')
        payload = BookCreatePayload(**data)

        with pytest.raises(AuthorNotFoundError):
            await self.creator.dispatch(payload)

    @pytest.mark.asyncio
    async def test_should_fail_when_editorial_not_found(self):
        self.repo_author.put(Ref.AuthorCervantes)

        data = self.loader.load('book')
        payload = BookCreatePayload(**data)

        with pytest.raises(EditorialNotFoundError):
            await self.creator.dispatch(payload)

    @pytest.mark.asyncio
    async def test_should_run_when_create(self):
        self.repo_author.put(Ref.AuthorCervantes)
        self.repo_editorial.put(Ref.EditorialAnaya)

        data = self.loader.load('book')
        payload = BookCreatePayload(**data)

        book = await self.creator.dispatch(payload)

        assert book.title == payload.title
        assert self.repo_book.stored is not None
