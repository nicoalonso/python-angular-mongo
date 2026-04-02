from pydantic import BaseModel, Field


class PurchaseInvoicePayload(BaseModel):
    """Payload for creating a purchase invoice."""
    number: str = Field(examples=['INV-001'])
    amount: float = Field(examples=[100.0])
    taxes: float = Field(examples=[20.0])
    total: float = Field(examples=[120.0])
