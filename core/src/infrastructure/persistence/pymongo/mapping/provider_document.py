from datetime import datetime
from typing import Optional

from pydantic import Field, ConfigDict

from src.domain.common import Address, EnterpriseContact
from src.domain.provider import Provider
from src.infrastructure.persistence.pymongo.mapping import MongoDocument
from .address_embed import AddressEmbed
from .enterprise_contact_embed import EnterpriseContactEmbed


class ProviderDocument(MongoDocument[Provider]):
    id: str = Field(alias="_id")
    name: str
    comercial_name: str = Field(alias="comercialName")
    contact: EnterpriseContactEmbed
    address: AddressEmbed
    vat_number: str = Field(alias="vatNumber")
    created_by: str = Field(alias="createdBy")
    created_at: datetime = Field(alias="createdAt")
    updated_by: Optional[str] = Field(default=None, alias="updatedBy")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)

    def to_domain(self) -> Provider:
        """
        Converts the ProviderDocument to a Provider domain model.
        :return: (Provider) domain model instance.
        """
        item = self.model_dump()
        item['address'] = Address(**item.pop('address'))
        item['contact'] = EnterpriseContact(**item.pop('contact'))

        return Provider(**item)
