from dataclasses import dataclass

from src.domain.identity import Identity, Collection
from src.domain.book import BookDescriptor, Book
from .purchase import Purchase


@dataclass
class PurchaseLine(Identity):
    """
    PurchaseLine entity represents a line item in a purchase
    """
    purchase: str = None
    book: BookDescriptor = None
    quantity: int = None
    unit_price: float = None
    discount_percentage: float = None
    total: float = None

    @classmethod
    def create(
            cls,
            purchase: Purchase,
            book: Book,
            quantity: int,
            unit_price: float,
            discount_percentage: float,
            total: float,
    ) -> "PurchaseLine":
        """
        Factory method to create a new PurchaseLine instance.
        """
        return cls(
            purchase=purchase.id,
            book=book.get_descriptor(),
            quantity=quantity,
            unit_price=unit_price,
            discount_percentage=discount_percentage,
            total=total,
        )

    def modify(
            self,
            book: Book,
            quantity: int,
            unit_price: float,
            discount_percentage: float,
            total: float,
    ) -> None:
        """
        Method to modify the purchase line details.
        """
        self.book = book.get_descriptor()
        self.quantity = quantity
        self.unit_price = unit_price
        self.discount_percentage = discount_percentage
        self.total = total


type PurchaseLineCollection = Collection[PurchaseLine]
