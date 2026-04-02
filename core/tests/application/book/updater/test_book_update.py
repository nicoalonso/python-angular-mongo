import pytest

from src.application.book.updater import BookUpdatePayload, BookUpdate
from src.domain.book.exception import BookNotFoundError
from tests.doubles.infrastructure.persistence import *
from tests.fixtures import FixturePayload, Ref


class TestBookUpdate:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_author = AuthorRepositoryStub()
        self.repo_editorial = EditorialRepositoryStub()
        self.repo_book = BookRepositoryStub(
            repo_author=self.repo_author,
            repo_editorial=self.repo_editorial,
        )
        repo_user = UserRepositoryStub()
        self.updater = BookUpdate(
            repo_book=self.repo_book,
            repo_author=self.repo_author,
            repo_editorial=self.repo_editorial,
            repo_user=repo_user,
        )

        loader = FixturePayload()
        data = loader.load('book')
        self.payload = BookUpdatePayload(**data)

    @pytest.mark.asyncio
    async def test_should_fail_when_not_found(self):
        with pytest.raises(BookNotFoundError):
            await self.updater.dispatch('invalid-id', self.payload)

    @pytest.mark.asyncio
    async def test_should_run_when_update(self):
        self.repo_book.put(Ref.BookRomeoAndJuliet)
        self.repo_author.put(Ref.AuthorShakespeare)
        self.repo_editorial.put(Ref.EditorialAnaya)

        await self.updater.dispatch('123456', self.payload)
