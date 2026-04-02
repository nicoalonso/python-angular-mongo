from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from src.domain.borrow.exception import InvalidBorrowNumberError
from src.domain.customer import CustomerDescriptor, Customer
from src.domain.identity import Entity, Collection

INTERVAL_DUE_DATE = 14  # Number of days until the due date for borrowed books


@dataclass
class Borrow(Entity):
    """
    Represents a borrow transaction in the library system.
    """
    customer: CustomerDescriptor = None
    number: str = None
    borrow_date: datetime = None
    total_books: int = 0
    due_date: datetime = None
    total_returned_books: int = 0
    returned: bool = False
    returned_date: Optional[datetime] = None
    penalty: bool = False
    penalty_amount: float = 0.0

    @classmethod
    def create(
            cls,
            customer: Customer,
            number: str,
            total_books: int,
            created_by: str,
    ) -> "Borrow":
        """
        Factory method to create a new Borrow instance.
        """
        cls._check(number)

        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days=INTERVAL_DUE_DATE)

        return cls(
            customer=customer.get_descriptor(),
            number=number,
            borrow_date=borrow_date,
            total_books=total_books,
            due_date=due_date,
            total_returned_books=0,
            returned=False,
            returned_date=None,
            penalty=False,
            penalty_amount=0.0,
            created_by=created_by,
        )

    @staticmethod
    def _check(number: str):
        """
        Validates the borrow transaction.
        :raises InvalidBorrowNumberError: If the borrow number is invalid (empty or whitespace).
        """
        if not number or not number.strip():
            raise InvalidBorrowNumberError()

    def modify(self, returned_books: int, updated_by: str) -> None:
        """Modifies the borrow transaction when books are returned."""
        self.total_returned_books = returned_books
        self.returned = self.total_returned_books >= self.total_books
        self.returned_date = datetime.now() if self.returned else None
        self.updated(updated_by)

    def penalize(self, amount: float) -> None:
        """Applies a penalty to the borrow transaction."""
        self.penalty = True
        self.penalty_amount = amount


type BorrowCollection = Collection[Borrow]
