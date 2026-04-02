import pytest

from src.application.book.reader import BookRead
from src.domain.book.exception import BookNotFoundError
from tests.doubles.infrastructure.persistence import BookRepositoryStub
from tests.fixtures import Ref


class TestBookRead:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_book = BookRepositoryStub()
        self.reader = BookRead(self.repo_book)

    @pytest.mark.asyncio
    async def test_should_fail_when_not_found(self):
        with pytest.raises(BookNotFoundError) as exc:
            await self.reader.dispatch('not-exists-id')

        assert str(exc.value) == 'Book with ID not-exists-id not found.'

    @pytest.mark.asyncio
    async def test_should_run_when_found(self):
        book = self.repo_book.put(Ref.BookRomeoAndJuliet)

        result = await self.reader.dispatch(book.id)

        assert result is not None
        assert result.id == book.id
