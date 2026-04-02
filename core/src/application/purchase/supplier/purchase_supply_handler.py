from typing import Union

from src.domain.bus import Handler
from src.application.purchase.creator import PurchaseCreatedEvent
from src.application.purchase.updater import PurchaseUpdatedEvent
from src.application.purchase.eraser import PurchaseDeletedEvent
from .purchase_supply import PurchaseSupply


class PurchaseSupplyHandler(Handler):
    """
    Handler for processing the supplying the purchase.
    """
    def __init__(self, supplier: PurchaseSupply):
        self.supplier = supplier

    async def handle(self, event: Union[PurchaseCreatedEvent, PurchaseUpdatedEvent, PurchaseDeletedEvent]):
        await self.supplier.dispatch(event.books)
