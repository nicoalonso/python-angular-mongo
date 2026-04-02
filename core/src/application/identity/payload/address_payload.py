from pydantic import BaseModel, Field


class AddressPayload(BaseModel):
    street: str = Field(examples=['123 Main St'])
    postal_code: str = Field(alias="postalCode", examples=['12345'])
    city: str = Field(examples=['Anytown'])
    province: str = Field(examples=['Anystate'])
    country: str = Field(examples=['USA'])
