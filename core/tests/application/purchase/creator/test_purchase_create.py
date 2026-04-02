import pytest

from src.application.purchase.creator import PurchaseCreatedEvent
from src.application.purchase.creator.purchase_create import PurchaseCreate
from src.application.purchase.creator.purchase_create_payload import PurchaseCreatePayload
from src.domain.book.exception import BookNotFoundError
from src.domain.provider.exception import ProviderNotFoundError
from src.domain.purchase.exception import PurchaseAlreadyExistsError
from tests.doubles.infrastructure.bus import DomainBusStub, assert_dispatch
from tests.doubles.infrastructure.persistence import *
from tests.fixtures import FixturePayload, Ref


class TestPurchaseCreate:
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
        self.creator = PurchaseCreate(
            repo_purchase=self.repo_purchase,
            repo_purchase_line=self.repo_purchase_line,
            repo_provider=self.repo_provider,
            repo_book=self.repo_book,
            repo_user=repo_user,
            bus=self.bus,
        )

        loader = FixturePayload()
        data = loader.load('purchase')
        self.payload = PurchaseCreatePayload(**data)

    @pytest.mark.asyncio
    async def test_should_fail_when_book_not_found(self):

        with pytest.raises(BookNotFoundError):
            await self.creator.dispatch(self.payload)

    @pytest.mark.asyncio
    async def test_should_fail_when_already_exists(self):
        self.repo_book.put(Ref.BookRomeoAndJuliet)
        self.repo_purchase.put(Ref.PurchaseBestBuyInv2)

        with pytest.raises(PurchaseAlreadyExistsError):
            await self.creator.dispatch(self.payload)

    @pytest.mark.asyncio
    async def test_should_fail_when_provider_not_found(self):
        self.repo_book.put(Ref.BookRomeoAndJuliet)

        with pytest.raises(ProviderNotFoundError):
            await self.creator.dispatch(self.payload)

    @pytest.mark.asyncio
    async def test_should_create_purchase(self):
        self.repo_book.put(Ref.BookRomeoAndJuliet)
        self.repo_provider.put(Ref.ProviderBestBuy)

        purchase = await self.creator.dispatch(self.payload)

        assert purchase.provider.name == 'Best Buy'
        assert self.repo_purchase.stored is not None
        assert self.repo_purchase_line.stored is not None
        assert_dispatch(self.bus, PurchaseCreatedEvent)
