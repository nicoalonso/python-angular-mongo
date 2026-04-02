import pytest

from src.application.book.eraser import BookDelete, BookAssociatedError
from src.domain.book.exception import BookNotFoundError
from tests.doubles.infrastructure.persistence import *
from tests.fixtures import Ref


class TestBookDelete:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_book = BookRepositoryStub()
        self.repo_purchase_line = PurchaseLineRepositoryStub()
        self.repo_sale_line = SaleLineRepositoryStub()
        self.repo_borrow_line = BorrowLineRepositoryStub()

        self.eraser = BookDelete(
            repo_book=self.repo_book,
            repo_purchase_line=self.repo_purchase_line,
            repo_sale_line=self.repo_sale_line,
            repo_borrow_line=self.repo_borrow_line,
        )

    @pytest.mark.asyncio
    async def test_should_fail_when_not_found(self):
        with pytest.raises(BookNotFoundError) as exc_info:
            await self.eraser.dispatch('non-existent-id')

        assert str(exc_info.value) == 'Book with ID non-existent-id not found.'

    @pytest.mark.asyncio
    async def test_should_fail_when_has_purchase_lines(self):
        self.repo_book.put(Ref.BookRomeoAndJuliet)
        self.repo_purchase_line.attach(Ref.PurchaseLineAmazonLine1)

        with pytest.raises(BookAssociatedError):
            await self.eraser.dispatch('book-id')

    @pytest.mark.asyncio
    async def test_should_fail_when_has_sale_lines(self):
        self.repo_book.put(Ref.BookRomeoAndJuliet)
        self.repo_sale_line.attach(Ref.SaleLineJohnDoe1Line1)

        with pytest.raises(BookAssociatedError):
            await self.eraser.dispatch('book-id')

    @pytest.mark.asyncio
    async def test_should_fail_when_has_borrow_lines(self):
        self.repo_book.put(Ref.BookRomeoAndJuliet)
        self.repo_borrow_line.attach(Ref.BorrowLineJohnQuijote)

        with pytest.raises(BookAssociatedError):
            await self.eraser.dispatch('book-id')

    @pytest.mark.asyncio
    async def test_should_delete_book(self):
        self.repo_book.put(Ref.BookRomeoAndJuliet)

        await self.eraser.dispatch('book-id')

        assert self.repo_book.removed is not None
