from src.domain.book import BookDescriptor
from src.domain.bus import DomainEvent
from src.domain.sale import Sale


class SaleCreatedEvent(DomainEvent):
    """
    Event triggered when a new sale is created.

    :ivar sale: The Sale object that was created.
    :ivar books: List of BookDescriptor objects representing the books involved in the sale.
    """
    def __init__(self, sale: Sale, books: list[BookDescriptor]):
        super().__init__('sale.created', 'sale')
        self.sale = sale
        self.books = books
