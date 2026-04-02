import pytest

from src.application.book.inventory import BookInventoryEvent
from src.application.sale.consumer import SaleConsume, SaleConsumeHandler
from src.application.sale.creator import SaleCreatedEvent
from tests.doubles.infrastructure.bus import DomainBusStub, assert_dispatch
from tests.fixtures.mothers import SaleMother, BookMother


class TestSaleConsumeHandler:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.bus = DomainBusStub()
        consumer = SaleConsume(self.bus)
        self.handler = SaleConsumeHandler(consumer)

    @pytest.mark.asyncio
    async def test_handle_sale_created_event(self):
        sale = SaleMother.john_doe_sale1()
        book = BookMother.don_quijote()
        event = SaleCreatedEvent(sale, [book.get_descriptor()])

        await self.handler.handle(event)

        assert_dispatch(self.bus, BookInventoryEvent)
