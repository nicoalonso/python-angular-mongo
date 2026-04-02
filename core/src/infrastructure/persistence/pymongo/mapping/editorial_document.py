from datetime import datetime
from typing import Optional

from pydantic import Field, ConfigDict

from src.domain.common import Address, EnterpriseContact
from src.domain.editorial import Editorial
from .address_embed import AddressEmbed
from .enterprise_contact_embed import EnterpriseContactEmbed
from .mongo_document import MongoDocument


class EditorialDocument(MongoDocument[Editorial]):
    id: str = Field(alias="_id")
    name: str
    comercial_name: str = Field(alias="comercialName")
    contact: EnterpriseContactEmbed
    address: AddressEmbed
    created_by: str = Field(alias="createdBy")
    created_at: datetime = Field(alias="createdAt")
    updated_by: Optional[str] = Field(default=None, alias="updatedBy")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)

    def to_domain(self) -> Editorial:
        """
        Converts the EditorialDocument to an Editorial domain model.
        :return: (Editorial) domain model instance.
        """
        item = self.model_dump()
        item['address'] = Address(**item.pop('address'))
        item['contact'] = EnterpriseContact(**item.pop('contact'))

        return Editorial(**item)
