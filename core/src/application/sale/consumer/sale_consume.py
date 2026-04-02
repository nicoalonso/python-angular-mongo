from src.application.book.inventory import BookInventoryEvent
from src.domain.book import BookDescriptor
from src.domain.bus import DomainBus


class SaleConsume:
    """
    Use case for consuming a sale.

    :ivar _bus: An instance of DomainBus for dispatching events related to the sale consumption process.
    """
    def __init__(self, bus: DomainBus):
        self._bus = bus

    async def dispatch(self, books: list[BookDescriptor]) -> None:
        """
        Dispatch book events for calculating inventory

        :param books: A list of BookDescriptor objects
        """
        for book in books:
            event = BookInventoryEvent(book)
            await self._bus.dispatch(event)
