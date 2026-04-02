from src.application.sale.creator import SaleCreatedEvent
from src.domain.bus.handler import Handler
from .sale_consume import SaleConsume


class SaleConsumeHandler(Handler):
    """
    Handler for processing the SaleCreatedEvent and consuming the sale.
    """
    def __init__(self, consumer: SaleConsume):
        self.consumer = consumer

    async def handle(self, event: SaleCreatedEvent) -> None:
        await self.consumer.dispatch(event.books)
