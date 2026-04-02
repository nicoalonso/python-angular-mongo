from datetime import datetime
from typing import Optional

from pydantic import Field, ConfigDict

from src.domain.common import Address
from src.domain.customer import Customer, ContactInfo, Membership
from src.infrastructure.persistence.pymongo.mapping import MongoDocument
from .address_embed import AddressEmbed
from .contact_info_embed import ContactInfoEmbed
from .membership_embed import MembershipEmbed


class CustomerDocument(MongoDocument[Customer]):
    id: str = Field(alias="_id")
    name: str
    surname: str
    membership: MembershipEmbed
    contact: ContactInfoEmbed
    address: AddressEmbed
    vat_number: str = Field(alias="vatNumber")
    created_by: str = Field(alias="createdBy")
    created_at: datetime = Field(alias="createdAt")
    updated_by: Optional[str] = Field(default=None, alias="updatedBy")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)

    def to_domain(self) -> Customer:
        """
        Converts the CustomerDocument to a Customer domain model.
        :return: (Customer) domain model instance.
        """
        item = self.model_dump()
        item['membership'] = Membership(**item.pop('membership'))
        item['contact'] = ContactInfo(**item.pop('contact'))
        item['address'] = Address(**item.pop('address'))

        return Customer(**item)
