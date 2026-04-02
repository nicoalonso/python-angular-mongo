from datetime import datetime
from typing import Optional

from pydantic import Field, ConfigDict

from src.domain.provider import ProviderDescriptor
from src.domain.purchase import Purchase, PurchaseInvoice
from .mongo_document import MongoDocument
from .provider_embed import ProviderEmbed
from .purchase_invoice_embed import PurchaseInvoiceEmbed


class PurchaseDocument(MongoDocument[Purchase]):
    """
    MongoDB document representation of the Purchase entity.
    """
    id: str = Field(alias="_id")
    provider: ProviderEmbed
    purchased_at: datetime = Field(alias="purchasedAt")
    invoice: PurchaseInvoiceEmbed
    created_by: str = Field(alias="createdBy")
    created_at: datetime = Field(alias="createdAt")
    updated_by: Optional[str] = Field(default=None, alias="updatedBy")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)

    def to_domain(self) -> Purchase:
        """
        Converts the PurchaseDocument to a Purchase domain model.
        :return: (Purchase) domain model instance.
        """
        item = self.model_dump()
        item['provider'] = ProviderDescriptor(**item.pop('provider'))
        item['invoice'] = PurchaseInvoice(**item.pop('invoice'))

        return Purchase(**item)
