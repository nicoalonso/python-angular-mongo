from src.domain.book import BookDescriptor
from src.domain.bus import DomainEvent, DomainRoute


class BookInventoryEvent(DomainEvent):
    """
    Event triggered when a book inventory change occurs.

    :ivar descriptor: A BookDescriptor object representing the book involved in the inventory change.
    """
    def __init__(self, descriptor: BookDescriptor):
        super().__init__('book.inventory', 'book', DomainRoute.LIBRARY)
        self.descriptor = descriptor
