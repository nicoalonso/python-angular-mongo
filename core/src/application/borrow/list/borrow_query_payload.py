from typing import Optional

from pydantic import Field

from src.domain.identity.list import ListQueryPayload


class BorrowQueryPayload(ListQueryPayload):
    """Borrow list filters"""
    customer_id: Optional[str] = Field(default=None, alias='customerId')
    customer: Optional[str] = None
    customer_number: Optional[str] = Field(default=None, alias='customerNumber')
    number: Optional[str] = None
    from_borrow_date: Optional[str] = Field(default=None, alias='fromBorrowDate')
    to_borrow_date: Optional[str] = Field(default=None, alias='toBorrowDate')
    from_due_date: Optional[str] = Field(default=None, alias='fromDueDate')
    to_due_date: Optional[str] = Field(default=None, alias='toDueDate')
    total_books: Optional[int] = Field(default=None, alias='totalBooks')
    returned: Optional[bool] = None
    penalty: Optional[bool] = None
