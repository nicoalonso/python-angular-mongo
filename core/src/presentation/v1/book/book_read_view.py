from dataclasses import asdict
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_serializer

from src.domain.book import Book
from src.presentation.identity import Result, format_date
from src.presentation.v1.author import AuthorDescriptorView
from src.presentation.v1.editorial import EditorialDescriptorView
from .book_detail_view import BookDetailView
from .book_sale_view import BookSaleView


class BookReadViewData(BaseModel):
    id: str = Field(examples=['123e4567-e89b-12d3-a456-426614174000'])
    title: str = Field(examples=['The Great Gatsby'])
    description: str = Field(examples=['A novel about the American dream.'])
    author: AuthorDescriptorView
    editorial: EditorialDescriptorView
    detail: BookDetailView
    sale: BookSaleView
    stock: int = Field(examples=[100, 50])
    created_by: str = Field(serialization_alias='createdBy', examples=['admin'])
    created_at: datetime = Field(serialization_alias='createdAt', examples=['2023-01-01T12:00:00+01:00'])
    updated_by: Optional[str] = Field(serialization_alias='updatedBy', examples=['admin'])
    updated_at: Optional[datetime] = Field(serialization_alias='updatedAt', examples=['2023-01-02T12:00:00+01:00'])

    @field_serializer("created_at", "updated_at", when_used="unless-none")
    def serialize_date(self, value: datetime) -> Optional[str]:
        """Serialize datetime to ISO format string"""
        return format_date(value)  # pragma: no cover


class BookReadView(Result[BookReadViewData]):
    def __init__(self, book: Book):
        super().__init__(data=BookReadViewData(**asdict(book)))
