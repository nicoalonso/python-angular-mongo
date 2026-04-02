from dataclasses import asdict
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_serializer

from src.domain.purchase import Purchase
from src.presentation.identity import Result, format_date
from src.presentation.v1.provider import ProviderDescriptorView
from .purchase_invoice_view import PurchaseInvoiceView


class PurchaseListViewData(BaseModel):
    id: str = Field(examples=['123e4567-e89b-12d3-a456-426614174000'])
    provider: ProviderDescriptorView
    purchased_at: datetime = Field(serialization_alias='purchasedAt', examples=['2024-01-01'])
    invoice: PurchaseInvoiceView
    created_by: str = Field(serialization_alias='createdBy', examples=['user123'])
    created_at: datetime = Field(serialization_alias='createdAt', examples=['2024-01-01T12:00:00+01:00'])
    updated_by: Optional[str] = Field(serialization_alias='updatedBy', examples=['user456'])
    updated_at: Optional[datetime] = Field(serialization_alias='updatedAt', examples=['2024-01-02T12:00:00+01:00'])

    @field_serializer("created_at", "updated_at", when_used="unless-none")
    def serialize_date(self, value: datetime) -> Optional[str]:
        """Serialize datetime to ISO format string"""
        return format_date(value)  # pragma: no cover


class PurchaseListView(Result[PurchaseListViewData]):
    def __init__(self, purchase: Purchase):
        super().__init__(data=PurchaseListViewData(**asdict(purchase)))
