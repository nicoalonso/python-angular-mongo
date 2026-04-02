from typing import Optional

from src.domain.purchase import PurchaseLine, PurchaseLineRepository
from src.domain.purchase.purchase_line import PurchaseLineCollection
from tests.fixtures import Ref
from tests.fixtures.mothers import PurchaseLineMother
from .entity_repository_stub import EntityRepositoryStub
from .book_repository_stub import BookRepositoryStub
from .purchase_repository_stub import PurchaseRepositoryStub


class PurchaseLineRepositoryStub(EntityRepositoryStub[PurchaseLine], PurchaseLineRepository):
    """
    Stub implementation of the PurchaseLineRepository for testing purposes.
    """
    def __init__(
            self,
            *,
            repo_purchase: Optional[PurchaseRepositoryStub] = None,
            repo_book: Optional[BookRepositoryStub] = None,
    ):
        self.repo_purchase = repo_purchase
        self.repo_book = repo_book

        super().__init__()

    async def obtain_by_purchase(self, purchase_id: str) -> PurchaseLineCollection:
        self.query_filter = purchase_id
        self._throw_error()
        return self.list

    async def obtain_by_book(self, book_id: str, limit: int | None = None) -> PurchaseLineCollection:
        self.query_filter = (book_id, limit)
        self._throw_error()
        return self.list

    def make_fixtures(self) -> None:
        purchase_amazon_inv1 = None
        purchase_best_buy_inv2 = None
        book_romeo_and_juliet = None
        book_don_quixote = None

        if self.repo_purchase:
            purchase_amazon_inv1 = self.repo_purchase.get(Ref.PurchaseAmazonInv1)
            purchase_best_buy_inv2 = self.repo_purchase.get(Ref.PurchaseBestBuyInv2)

        if self.repo_book:
            book_romeo_and_juliet = self.repo_book.get(Ref.BookRomeoAndJuliet)
            book_don_quixote = self.repo_book.get(Ref.BookDonQuijote)

        amazon_line1 = PurchaseLineMother.amazon_line1(
            purchase=purchase_amazon_inv1,
            book=book_romeo_and_juliet,
        )
        self.add_fixture(Ref.PurchaseLineAmazonLine1, amazon_line1)

        amazon_line2 = PurchaseLineMother.amazon_line2(
            purchase=purchase_amazon_inv1,
            book=book_don_quixote,
        )
        self.add_fixture(Ref.PurchaseLineAmazonLine2, amazon_line2)

        best_buy_line1 = PurchaseLineMother.best_buy_line1(
            purchase=purchase_best_buy_inv2,
            book=book_romeo_and_juliet,
        )
        self.add_fixture(Ref.PurchaseLineBestBuyLine1, best_buy_line1)
