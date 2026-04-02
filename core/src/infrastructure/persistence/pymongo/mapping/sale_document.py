from datetime import datetime
from typing import Optional

from pydantic import Field, ConfigDict

from src.domain.customer import CustomerDescriptor
from src.domain.sale import Sale, SaleInvoice
from src.infrastructure.persistence.pymongo.mapping import MongoDocument
from .customer_embed import CustomerEmbed
from .sale_invoice_embed import SaleInvoiceEmbed


class SaleDocument(MongoDocument[Sale]):
    """
    MongoDB document representation of the Sale entity.
    """
    id: str = Field(alias="_id")
    customer: CustomerEmbed
    number: str
    invoice: SaleInvoiceEmbed
    created_by: str = Field(alias="createdBy")
    created_at: datetime = Field(alias="createdAt")
    updated_by: Optional[str] = Field(default=None, alias="updatedBy")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)

    def to_domain(self) -> Sale:
        """
        Converts the SaleDocument to a Sale domain model.
        :return: (Sale) domain model instance.
        """
        item = self.model_dump()
        item['customer'] = CustomerDescriptor(**item.pop('customer'))
        item['invoice'] = SaleInvoice(**item.pop('invoice'))

        return Sale(**item)
