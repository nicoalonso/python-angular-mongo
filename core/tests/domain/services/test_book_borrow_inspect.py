import pytest

from src.domain.services.book_inspector import BookBorrowInspect
from tests.doubles.infrastructure.persistence import BorrowLineRepositoryStub
from tests.fixtures import Ref
from tests.fixtures.mothers import BookMother


class TestBookSaleInspect:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_borrow_line = BorrowLineRepositoryStub()
        self.inspector = BookBorrowInspect(self.repo_borrow_line)

    @pytest.mark.asyncio
    async def test_should_false_when_not_stock(self):
        book = BookMother.romeo_and_juliet()

        result = await self.inspector.available(book)

        assert result is False

    @pytest.mark.asyncio
    async def test_should_true_when_has_stock_not_active_borrows(self):
        book = BookMother.romeo_and_juliet()
        book.change_stock(3)

        result = await self.inspector.available(book)

        assert result is True

    @pytest.mark.asyncio
    async def test_should_true_when_has_stock_and_active_borrows(self):
        self.repo_borrow_line.attach(Ref.BorrowLineJohnQuijote)

        book = BookMother.romeo_and_juliet()
        book.change_stock(4)

        result = await self.inspector.available(book)

        assert result is True

    @pytest.mark.asyncio
    async def test_should_false_when_has_stock_is_equals_to_active_borrows(self):
        self.repo_borrow_line.attach(Ref.BorrowLineJohnQuijote)
        self.repo_borrow_line.attach(Ref.BorrowLineJohnRomeoAndJuliet)

        book = BookMother.romeo_and_juliet()
        book.change_stock(2)

        result = await self.inspector.available(book)

        assert result is False
