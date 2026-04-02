import pytest

from src.application.book.inventory import BookInventoryEvent
from src.application.purchase.creator import PurchaseCreatedEvent
from src.application.purchase.supplier import PurchaseSupply, PurchaseSupplyHandler
from tests.doubles.infrastructure.bus import DomainBusStub, assert_dispatch
from tests.fixtures.mothers import BookMother, PurchaseMother


class TestPurchaseSupplyHandler:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.bus = DomainBusStub()
        supplier = PurchaseSupply(self.bus)
        self.handler = PurchaseSupplyHandler(supplier)

    @pytest.mark.asyncio
    async def test_handle_purchase_created_event(self):
        purchase = PurchaseMother.amazon_inv1()
        book = BookMother.romeo_and_juliet()
        event = PurchaseCreatedEvent(purchase, [book.get_descriptor()])

        await self.handler.handle(event)

        assert_dispatch(self.bus, BookInventoryEvent)
