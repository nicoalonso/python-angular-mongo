from pydantic import BaseModel, Field, ConfigDict


class AddressEmbed(BaseModel):
    street: str
    postal_code: str = Field(alias="postalCode")
    city: str
    province: str
    country: str

    model_config = ConfigDict(populate_by_name=True)
