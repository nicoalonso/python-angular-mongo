from pydantic import BaseModel


class PurchaseInvoiceEmbed(BaseModel):
    number: str
    amount: float
    taxes: float
    total: float
