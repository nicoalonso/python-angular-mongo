from typing import Optional

from pydantic import Field

from src.domain.identity.list import ListQueryPayload


class PurchaseQueryPayload(ListQueryPayload):
    """Purchase list filters"""
    provider: Optional[str] = None
    from_purchased_at: Optional[str] = Field(default=None, alias='fromPurchasedAt')
    to_purchased_at: Optional[str] = Field(default=None, alias='toPurchasedAt')
    invoice_number: Optional[str] = Field(default=None, alias='invoiceNumber')
