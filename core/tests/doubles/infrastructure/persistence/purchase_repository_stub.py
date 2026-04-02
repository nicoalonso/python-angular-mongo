from typing import Optional

from src.domain.purchase import Purchase, PurchaseRepository
from src.domain.purchase.purchase import PurchaseCollection
from tests.fixtures import Ref
from tests.fixtures.mothers import PurchaseMother
from .provider_repository_stub import ProviderRepositoryStub
from .entity_repository_stub import EntityRepositoryStub


class PurchaseRepositoryStub(EntityRepositoryStub[Purchase], PurchaseRepository):
    """
    Stub implementation of the PurchaseRepository for testing purposes.

    :ivar repo_provider: Optional[ProviderRepositoryStub] - An optional reference to a ProviderRepositoryStub for resolving provider-related queries.
    """
    def __init__(
            self,
            *,
            repo_provider: Optional[ProviderRepositoryStub] = None,
    ):
        self.repo_provider = repo_provider

        super().__init__()

    async def obtain_by_provider_and_number(self, provider_id: str, invoice_number: str) -> Purchase | None:
        self.query_filter = (provider_id, invoice_number)
        self._throw_error()
        return self.read

    async def obtain_by_provider(self, provider_id: str, limit: int | None = None) -> PurchaseCollection:
        self.query_filter = (provider_id, limit)
        self._throw_error()
        return self.list

    def make_fixtures(self) -> None:
        amazon = None
        best_buy = None

        if self.repo_provider:
            amazon = self.repo_provider.get(Ref.ProviderAmazon)
            best_buy = self.repo_provider.get(Ref.ProviderBestBuy)

        purchase_amazon_inv1 = PurchaseMother.amazon_inv1(provider=amazon)
        self.add_fixture(Ref.PurchaseAmazonInv1, purchase_amazon_inv1)

        purchase_best_buy_inv2 = PurchaseMother.best_buy_inv2(provider=best_buy)
        self.add_fixture(Ref.PurchaseBestBuyInv2, purchase_best_buy_inv2)
