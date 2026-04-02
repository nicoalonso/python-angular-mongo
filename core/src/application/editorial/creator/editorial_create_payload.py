from pydantic import BaseModel, Field

from src.application.identity.payload import EnterpriseContactPayload, AddressPayload


class EditorialCreatePayload(BaseModel):
    """Payload for creating an editorial."""
    name: str = Field(examples=['Editorial XYZ'])
    comercial_name: str = Field(alias="comercialName", examples=['Editorial XYZ'])
    contact: EnterpriseContactPayload
    address: AddressPayload
