from typing import Annotated

from fastapi import Depends

from src.application.purchase.creator import PurchaseCreatedEvent
from src.application.purchase.eraser import PurchaseDeletedEvent
from src.application.purchase.supplier import PurchaseSupplyHandler
from src.application.purchase.updater import PurchaseUpdatedEvent
from src.application.sale.consumer import SaleConsumeHandler
from src.application.sale.creator import SaleCreatedEvent
from src.domain.bus import DomainBus
from src.infrastructure.dependencies.bus import get_bus
from src.infrastructure.dependencies.purchase import get_purchase_supply_handler
from src.infrastructure.dependencies.sale import get_sale_consume_handler


def handlers_register(
        bus: Annotated[DomainBus, Depends(get_bus)],
        consume_handler: Annotated[SaleConsumeHandler, Depends(get_sale_consume_handler)],
        supply_handler: Annotated[PurchaseSupplyHandler, Depends(get_purchase_supply_handler)],
) -> None:
    if not bus.initialize:
        return

    bus.register_handler(SaleCreatedEvent, consume_handler)
    bus.register_handler(PurchaseCreatedEvent, supply_handler)
    bus.register_handler(PurchaseUpdatedEvent, supply_handler)
    bus.register_handler(PurchaseDeletedEvent, supply_handler)
    bus.registered()
