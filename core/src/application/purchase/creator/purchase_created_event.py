from src.domain.book import BookDescriptor
from src.domain.bus import DomainEvent
from src.domain.purchase import Purchase


class PurchaseCreatedEvent(DomainEvent):
    """
    Event triggered when a new purchase is created.
    """
    def __init__(self, purchase: Purchase, books: list[BookDescriptor]):
        super().__init__('purchase.created', 'purchase')
        self.purchase = purchase
        self.books = books
