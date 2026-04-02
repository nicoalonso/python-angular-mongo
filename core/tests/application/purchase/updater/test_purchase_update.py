import pytest

from src.application.purchase.updater import PurchaseUpdatePayload, PurchaseUpdate, PurchaseUpdatedEvent
from tests.doubles.infrastructure.bus import DomainBusStub, assert_dispatch
from tests.doubles.infrastructure.persistence import *
from tests.fixtures import FixturePayload, Ref


class TestPurchaseUpdate:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_provider = ProviderRepositoryStub()
        self.repo_purchase = PurchaseRepositoryStub(repo_provider=self.repo_provider)
        self.repo_book = BookRepositoryStub()
        self.repo_purchase_line = PurchaseLineRepositoryStub(
            repo_purchase=self.repo_purchase,
            repo_book=self.repo_book,
        )
        self.bus = DomainBusStub()
        repo_user = UserRepositoryStub()

        self.updater = PurchaseUpdate(
            repo_purchase=self.repo_purchase,
            repo_purchase_line=self.repo_purchase_line,
            repo_provider=self.repo_provider,
            repo_book=self.repo_book,
            repo_user=repo_user,
            bus=self.bus,
        )

        self.loader = FixturePayload()

    @pytest.mark.asyncio
    async def test_should_fail_when_purchase_not_found(self):
        data = self.loader.load('purchase')
        payload = PurchaseUpdatePayload(**data)

        with pytest.raises(Exception):
            await self.updater.dispatch('non-existent-id', payload)

    @pytest.mark.asyncio
    async def test_should_update_purchase(self):
        self.repo_provider.put(Ref.ProviderAmazon)
        self.repo_book.put(Ref.BookRomeoAndJuliet)

        self.repo_purchase.put(Ref.PurchaseBestBuyInv2)
        line1 = self.repo_purchase_line.attach(Ref.PurchaseLineAmazonLine1)
        self.repo_purchase_line.attach(Ref.PurchaseLineAmazonLine2)

        data = self.loader.load('purchase')
        data['lines'][0]['lineId'] = line1.id
        payload = PurchaseUpdatePayload(**data)

        await self.updater.dispatch('12356', payload)

        assert self.repo_purchase.stored is not None
        assert self.repo_purchase_line.stored is not None
        assert self.repo_purchase_line.removed is not None
        assert_dispatch(self.bus, PurchaseUpdatedEvent)
