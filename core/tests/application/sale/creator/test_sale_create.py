import pytest

from src.application.sale.creator import SaleCreate, SaleCreatePayload, SaleCreatedEvent
from src.domain.book.exception import BookNotFoundError
from src.domain.customer.exception import CustomerNotFoundError
from src.domain.sale.exception import SaleLinesEmptyError
from tests.doubles.infrastructure.bus import DomainBusStub, assert_dispatch
from tests.doubles.infrastructure.persistence import *
from tests.fixtures import FixturePayload, Ref


class TestSaleCreate:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.loader = FixturePayload()
        self.repo_customer = CustomerRepositoryStub()
        self.repo_sale = SaleRepositoryStub(repo_customer=self.repo_customer)
        self.repo_book = BookRepositoryStub()
        self.repo_sale_line = SaleLineRepositoryStub(
            repo_sale=self.repo_sale,
            repo_book=self.repo_book,
        )
        self.bus = DomainBusStub()
        repo_sequence = SequenceNumberRepositoryStub()
        repo_user = UserRepositoryStub()

        self.creator = SaleCreate(
            repo_sale=self.repo_sale,
            repo_sale_line=self.repo_sale_line,
            repo_customer=self.repo_customer,
            repo_book=self.repo_book,
            repo_sequence_number=repo_sequence,
            repo_user=repo_user,
            bus=self.bus,
        )

    @pytest.mark.asyncio
    async def test_should_fail_when_empty_lines(self):
        data = self.loader.override(lines=[]).load('sale')
        payload = SaleCreatePayload(**data)

        with pytest.raises(SaleLinesEmptyError):
            await self.creator.dispatch(payload)

    @pytest.mark.asyncio
    async def test_should_fail_when_book_not_found(self):
        data = self.loader.load('sale')
        payload = SaleCreatePayload(**data)

        with pytest.raises(BookNotFoundError):
            await self.creator.dispatch(payload)

    @pytest.mark.asyncio
    async def test_should_fail_when_customer_not_found(self):
        self.repo_book.put(Ref.BookRomeoAndJuliet)

        data = self.loader.load('sale')
        payload = SaleCreatePayload(**data)

        with pytest.raises(CustomerNotFoundError):
            await self.creator.dispatch(payload)

    @pytest.mark.asyncio
    async def test_should_run_when_create(self):
        self.repo_book.put(Ref.BookRomeoAndJuliet)
        self.repo_customer.put(Ref.CustomerJohnDoe)

        data = self.loader.load('sale')
        payload = SaleCreatePayload(**data)

        sale = await self.creator.dispatch(payload)

        assert sale.invoice.total == 121
        assert self.repo_sale.stored is not None
        assert self.repo_sale_line.stored is not None
        assert_dispatch(self.bus, SaleCreatedEvent)
