from pydantic import BaseModel, Field

from src.application.sale.creator.payload import SaleInvoicePayload, SaleLinePayload


class SaleCreatePayload(BaseModel):
    """Payload for creating a sale."""
    customer_id: str = Field(alias="customerId", examples=['123e4567-e89b-12d3-a456-426614174000'])
    invoice: SaleInvoicePayload
    lines: list[SaleLinePayload]
