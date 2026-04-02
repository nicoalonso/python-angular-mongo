from pydantic import BaseModel, Field


class CustomerDescriptorView(BaseModel):
    """Customer descriptor read view data"""
    id: str = Field(examples=['123e4567-e89b-12d3-a456-426614174000'])
    name: str = Field(examples=['John'])
    surname: str = Field(examples=['Doe'])
    vat_number: str = Field(serialization_alias='vatNumber',examples=['1234567890A'])
    number: str = Field(examples=['SN-00001'])
