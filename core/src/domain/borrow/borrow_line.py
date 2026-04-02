from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.domain.book import BookDescriptor, Book
from src.domain.identity import Identity, Collection
from .borrow import Borrow


@dataclass
class BorrowLine(Identity):
    """
    BorrowLine entity represents a line item in a borrow transaction
    """
    borrow: str = None
    book: BookDescriptor = None
    returned: bool = False
    returned_date: Optional[datetime] = None
    penalty: bool = False
    penalty_amount: float = 0.0

    @classmethod
    def create(cls, borrow: Borrow, book: Book) -> "BorrowLine":
        """
        Factory method to create a new BorrowLine instance.
        """
        return cls(
            borrow=borrow.id,
            book=book.get_descriptor(),
            returned=False,
            returned_date=None,
            penalty=False,
            penalty_amount=0.0,
        )

    def check_in(self):
        """
        Method to check in the borrowed book.
        """
        self.returned = True
        self.returned_date = datetime.now()

    def penalize(self, amount: float):
        """
        Method to apply a penalty to the borrow line.
        """
        self.penalty = True
        self.penalty_amount = amount


type BorrowLineCollection = Collection[BorrowLine]
