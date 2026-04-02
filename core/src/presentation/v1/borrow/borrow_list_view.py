from dataclasses import asdict
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_serializer, Field

from src.domain.borrow import Borrow
from src.presentation.identity import Result, format_date, format_short_date
from src.presentation.v1.customer import CustomerDescriptorView


class BorrowListViewData(BaseModel):
    id: str = Field(examples=['123e4567-e89b-12d3-a456-426614174000'])
    customer: CustomerDescriptorView
    number: str = Field(examples=['P-00001'])
    borrow_date: datetime = Field(serialization_alias='borrowDate', examples=['2024-01-01'])
    total_books: int = Field(serialization_alias='totalBooks', examples=['3'])
    due_date: datetime = Field(serialization_alias='dueDate', examples=['2024-01-15'])
    total_returned_books: int = Field(serialization_alias='totalReturnedBooks', examples=['2'])
    returned: bool = Field(examples=[True])
    returned_date: Optional[datetime] = Field(serialization_alias='returnedDate', examples=['2024-01-10'])
    penalty: bool = Field(examples=[False])
    penalty_amount: int = Field(serialization_alias='penaltyAmount', examples=[15.0])
    created_by: str = Field(serialization_alias='createdBy', examples=['admin'])
    created_at: datetime = Field(serialization_alias='createdAt', examples=['2024-01-01T10:00:00+01:00'])
    updated_by: Optional[str] = Field(serialization_alias='updatedBy', examples=['admin'])
    updated_at: Optional[datetime] = Field(serialization_alias='updatedAt', examples=['2024-01-02T12:00:00+01:00'])

    @field_serializer("borrow_date", "due_date", "returned_date", when_used="unless-none")
    def serialize_short_date(self, value: datetime) -> Optional[str]:
        """Serialize datetime to ISO format string"""
        return format_short_date(value)  # pragma: no cover

    @field_serializer("created_at", "updated_at", when_used="unless-none")
    def serialize_date(self, value: datetime) -> Optional[str]:
        """Serialize datetime to ISO format string"""
        return format_date(value)  # pragma: no cover


class BorrowListView(Result[BorrowListViewData]):
    def __init__(self, borrow: Borrow):
        super().__init__(data=BorrowListViewData(**asdict(borrow)))
