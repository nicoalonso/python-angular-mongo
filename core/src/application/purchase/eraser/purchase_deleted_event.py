from src.domain.book import BookDescriptor
from src.domain.bus import DomainEvent
from src.domain.purchase import Purchase


class PurchaseDeletedEvent(DomainEvent):
    """
    Event triggered when a purchase is deleted.
    """
    def __init__(self, purchase: Purchase, books: list[BookDescriptor]):
        super().__init__('purchase.deleted', 'purchase')
        self.purchase = purchase
        self.books = books
