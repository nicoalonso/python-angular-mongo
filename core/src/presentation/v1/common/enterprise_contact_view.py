from pydantic import BaseModel, Field


class EnterpriseContactView(BaseModel):
    email: str = Field(examples=['jdoe@gmail.com'])
    website: str = Field(examples=['https://www.jdoe.com'])
    phone1: str = Field(examples=['+1-555-555-5555'])
    phone2: str = Field(examples=['+1-555-555-5555'])
