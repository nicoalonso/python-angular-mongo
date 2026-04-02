from typing import Optional

from src.domain.sale import SaleLine, SaleLineRepository, SaleLineCollection
from tests.fixtures import Ref
from tests.fixtures.mothers import SaleLineMother
from .entity_repository_stub import EntityRepositoryStub
from .sale_repository_stub import SaleRepositoryStub
from .book_repository_stub import BookRepositoryStub


class SaleLineRepositoryStub(EntityRepositoryStub[SaleLine], SaleLineRepository):
    """
    Stub implementation of the SaleLineRepository for testing purposes.
    """
    def __init__(
            self,
            *,
            repo_sale: Optional[SaleRepositoryStub] = None,
            repo_book: Optional[BookRepositoryStub] = None,
    ):
        self.repo_sale = repo_sale
        self.repo_book = repo_book

        super().__init__()

    async def obtain_by_sale(self, sale_id: str) -> SaleLineCollection:
        self.query_filter = sale_id
        self._throw_error()
        return self.list

    async def obtain_by_book(self, book_id: str, limit: int | None = None) -> SaleLineCollection:
        self.query_filter = (book_id, limit)
        self._throw_error()
        return self.list

    def make_fixtures(self) -> None:
        john_doe_sale1 = None
        john_doe_sale2 = None
        book_romeo_and_juliet = None
        book_don_quixote = None

        if self.repo_sale:
            john_doe_sale1 = self.repo_sale.get(Ref.SaleJohnDoe1)
            john_doe_sale2 = self.repo_sale.get(Ref.SaleJohnDoe2)

        if self.repo_book:
            book_romeo_and_juliet = self.repo_book.get(Ref.BookRomeoAndJuliet)
            book_don_quixote = self.repo_book.get(Ref.BookDonQuijote)

        john_doe_sale1_line1 = SaleLineMother.john_sale1_line1(sale=john_doe_sale1, book=book_romeo_and_juliet)
        self.add_fixture(Ref.SaleLineJohnDoe1Line1, john_doe_sale1_line1)

        john_doe_sale1_line2 = SaleLineMother.john_sale1_line2(sale=john_doe_sale1, book=book_don_quixote)
        self.add_fixture(Ref.SaleLineJohnDoe1Line2, john_doe_sale1_line2)

        john_doe_sale2_line1 = SaleLineMother.john_sale2_line1(sale=john_doe_sale2, book=book_romeo_and_juliet)
        self.add_fixture(Ref.SaleLineJohnDoe2Line1, john_doe_sale2_line1)
