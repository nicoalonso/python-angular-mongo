from dataclasses import dataclass

from src.domain.book import BookDescriptor, Book
from src.domain.identity import Identity, Collection
from .sale import Sale


@dataclass
class SaleLine(Identity):
    """
    SaleLine entity represents a line item in a sale
    """
    sale: str = None
    book: BookDescriptor = None
    quantity: int = None
    price: float = None
    discount: float = None
    total: float = None

    @classmethod
    def create(
            cls,
            sale: Sale,
            book: Book,
            quantity: int,
            price: float,
            discount: float,
            total: float,
    ) -> "SaleLine":
        """
        Factory method to create a new SaleLine instance.
        """
        return cls(
            sale=sale.id,
            book=book.get_descriptor(),
            quantity=quantity,
            price=price,
            discount=discount,
            total=total,
        )

    def modify(
            self,
            book: Book,
            quantity: int,
            price: float,
            discount: float,
            total: float,
    ) -> None:
        """
        Method to modify the sale line details.
        """
        self.book = book.get_descriptor()
        self.quantity = quantity
        self.price = price
        self.discount = discount
        self.total = total


type SaleLineCollection = Collection[SaleLine]
