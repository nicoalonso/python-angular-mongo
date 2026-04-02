from src.application.book.inventory import BookInventoryEvent
from src.domain.book import BookDescriptor
from src.domain.bus import DomainBus


class PurchaseSupply:
    """
    Use case for supply a purchase
    """
    def __init__(self, bus: DomainBus):
        self._bus = bus

    async def dispatch(self, books: list[BookDescriptor]) -> None:
        """
        Dispatch book events for calculating inventory
        :param books: A list of BookDescriptor
        """
        for book in books:
            event = BookInventoryEvent(book)
            await self._bus.dispatch(event)
