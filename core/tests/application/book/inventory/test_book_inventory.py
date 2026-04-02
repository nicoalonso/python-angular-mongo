import pytest

from src.application.book.inventory import BookInventory
from src.domain.book.exception import BookNotFoundError
from tests.doubles.infrastructure.persistence import BookRepositoryStub, PurchaseLineRepositoryStub, \
    SaleLineRepositoryStub
from tests.fixtures import Ref
from tests.fixtures.mothers import BookMother, PurchaseLineMother, SaleLineMother


class TestBookInventory:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_book = BookRepositoryStub()
        self.repo_purchase_line = PurchaseLineRepositoryStub()
        self.repo_sale_line = SaleLineRepositoryStub()

        self.inventory = BookInventory(
            repo_book=self.repo_book,
            repo_purchase_line=self.repo_purchase_line,
            repo_sale_line=self.repo_sale_line,
        )

    @pytest.mark.asyncio
    async def test_fail_when_book_not_found(self):
        book = BookMother.romeo_and_juliet()

        with pytest.raises(BookNotFoundError):
            await self.inventory.dispatch(book.get_descriptor())

    @pytest.mark.asyncio
    async def test_should_zero_stock_when_lines_not_found(self):
        book = self.repo_book.put(Ref.BookRomeoAndJuliet)

        await self.inventory.dispatch(book.get_descriptor())

        assert self.repo_book.stored is not None
        assert self.repo_book.stored.stock == 0

    @pytest.mark.asyncio
    async def test_should_stock_positive_when_has_purchase_lines(self):
        book = self.repo_book.put(Ref.BookRomeoAndJuliet)
        self.repo_purchase_line.attach(Ref.PurchaseLineAmazonLine1)

        await self.inventory.dispatch(book.get_descriptor())

        assert self.repo_book.stored is not None
        assert self.repo_book.stored.stock == 2

    @pytest.mark.asyncio
    async def test_should_stock_positive_when_has_purchase_and_sale(self):
        book = self.repo_book.put(Ref.BookRomeoAndJuliet)
        self.repo_purchase_line.attach(Ref.PurchaseLineAmazonLine1)
        self.repo_sale_line.attach(Ref.SaleLineJohnDoe1Line2)

        await self.inventory.dispatch(book.get_descriptor())

        assert self.repo_book.stored is not None
        assert self.repo_book.stored.stock == 1

    @pytest.mark.asyncio
    async def test_should_stock_zero_when_has_purchase_and_sale_lines(self):
        book = self.repo_book.put(Ref.BookRomeoAndJuliet)

        purchase_line = PurchaseLineMother.amazon_line1(book=book, quantity=2)
        self.repo_purchase_line.manual_put(purchase_line)

        sale_line = SaleLineMother.john_sale1_line1(book=book, quantity=2)
        self.repo_sale_line.manual_put(sale_line)

        await self.inventory.dispatch(book.get_descriptor())

        assert self.repo_book.stored is not None
        assert self.repo_book.stored.stock == 0

    @pytest.mark.asyncio
    async def test_should_stock_zero_when_has_only_sale_lines(self):
        book = self.repo_book.put(Ref.BookRomeoAndJuliet)
        self.repo_sale_line.attach(Ref.SaleLineJohnDoe1Line2)

        await self.inventory.dispatch(book.get_descriptor())

        assert self.repo_book.stored is not None
        assert self.repo_book.stored.stock == 0
