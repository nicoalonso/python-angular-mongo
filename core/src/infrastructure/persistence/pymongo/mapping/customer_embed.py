from pydantic import BaseModel, Field, ConfigDict


class CustomerEmbed(BaseModel):
    id: str
    name: str
    surname: str
    vat_number: str = Field(alias="vatNumber")
    number: str

    model_config = ConfigDict(populate_by_name=True)
