from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_serializer

from src.presentation.identity import format_short_date


class SaleInvoiceView(BaseModel):
    date: datetime = Field(examples=['2024-01-01'])
    amount: float = Field(examples=[100.0])
    tax_percentage: float = Field(serialization_alias='taxPercentage', examples=[20.0])
    taxes: float = Field(examples=[20.0])
    total: float = Field(examples=[120.0])

    @field_serializer("date", when_used="unless-none")
    def serialize_date(self, value: datetime) -> Optional[str]:
        """Serialize datetime to ISO format string"""
        return format_short_date(value)  # pragma: no cover
