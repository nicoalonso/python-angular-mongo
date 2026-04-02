from pydantic import BaseModel, Field

from src.application.identity.payload import EnterpriseContactPayload, AddressPayload


class ProviderCreatePayload(BaseModel):
    """Payload for creating a provider."""
    name: str = Field(examples=['Amazon'])
    comercial_name: str = Field(alias="comercialName", examples=['Amazon Inc.'])
    contact: EnterpriseContactPayload
    address: AddressPayload
    vat_number: str = Field(alias="vatNumber", examples=['B123456789'])
