import logging

from src.domain.bus import Handler
from .book_inventory import BookInventory
from .book_inventory_event import BookInventoryEvent


class BookInventoryHandler(Handler):
    """
    Handler for book inventory related domain events.
    """
    def __init__(self, inventory: BookInventory):
        self.inventory = inventory
        self.log = logging.getLogger('uvicorn')

    async def handle(self, event: BookInventoryEvent):
        try:
            await self.inventory.dispatch(event.descriptor)
        except Exception as e:
            self.log.error(f"Error handling event {event.descriptor.id}: {e}")
