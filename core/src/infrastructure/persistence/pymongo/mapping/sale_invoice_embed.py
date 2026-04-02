from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class SaleInvoiceEmbed(BaseModel):
    date: datetime
    amount: float
    tax_percentage: float = Field(alias="taxPercentage")
    taxes: float
    total: float

    model_config = ConfigDict(populate_by_name=True)
