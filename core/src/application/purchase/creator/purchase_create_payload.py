from datetime import datetime

from pydantic import BaseModel, Field

from src.application.purchase.creator.payload import PurchaseInvoicePayload, PurchaseLinePayload


class PurchaseCreatePayload(BaseModel):
    """Payload for creating a purchase."""
    provider_id: str = Field(alias="providerId", examples=['123e4567-e89b-12d3-a456-426614174000'])
    purchased_at: datetime = Field(alias="purchasedAt", examples=['2024-01-01'])
    invoice: PurchaseInvoicePayload
    lines: list[PurchaseLinePayload]
