from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_serializer

from src.presentation.identity import format_short_date


class BookDetailView(BaseModel):
    edition: str = Field(examples=['First Edition', 'Second Edition'])
    isbn: str = Field(examples=['978-3161484100'])
    language: str = Field(examples=['English', 'Spanish'])
    published_at: datetime = Field(serialization_alias='publishedAt', examples=['2023-01-01'])
    pages: int = Field(examples=[350, 500])

    @field_serializer("published_at", when_used="unless-none")
    def serialize_date(self, value: datetime) -> Optional[str]:
        """Serialize datetime to ISO format string"""
        return format_short_date(value)  # pragma: no cover
