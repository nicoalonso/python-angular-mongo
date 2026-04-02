import pytest

from src.application.book.available import BookAvailable
from src.domain.book.exception import BookNotFoundError
from src.domain.services.book_inspector import BookInspectFactory
from tests.doubles.infrastructure.persistence import BookRepositoryStub, BorrowLineRepositoryStub
from tests.fixtures import Ref


class TestBookAvailable:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_book = BookRepositoryStub()
        repo_borrow_line = BorrowLineRepositoryStub(repo_book=self.repo_book)
        factory = BookInspectFactory(repo_borrow_line=repo_borrow_line)
        self.available = BookAvailable(self.repo_book, factory)

    @pytest.mark.asyncio
    async def test_should_fail_when_not_found(self):
        with pytest.raises(BookNotFoundError) as exc:
            await self.available.dispatch("invalid-id", is_sale=False)

        assert str(exc.value) == "Book with ID invalid-id not found."

    @pytest.mark.asyncio
    async def test_should_return_true_when_available(self):
        book = self.repo_book.put(Ref.BookDonQuijote)
        book.change_stock(10)

        result = await self.available.dispatch(book.id, is_sale=True)

        assert result is True
