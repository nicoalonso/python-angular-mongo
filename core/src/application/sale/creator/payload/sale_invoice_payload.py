from datetime import datetime

from pydantic import BaseModel, Field


class SaleInvoicePayload(BaseModel):
    """Payload for creating a sale invoice."""
    date: datetime = Field(examples=['2024-06-01'])
    amount: float = Field(examples=[100.0])
    tax_percentage: float = Field(alias="taxPercentage", examples=[10.0])
    taxes: float = Field(examples=[10.0])
    total: float = Field(examples=[110.0])
