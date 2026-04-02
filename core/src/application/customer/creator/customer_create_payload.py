from pydantic import BaseModel, Field

from src.application.customer.creator.payload import ContactPayload
from src.application.identity.payload import AddressPayload


class CustomerCreatePayload(BaseModel):
    """Payload for creating a new customer."""
    name: str = Field(examples=['John'])
    surname: str = Field(examples=['Doe'])
    contact: ContactPayload
    address: AddressPayload
    vat_number: str = Field(alias="vatNumber")
