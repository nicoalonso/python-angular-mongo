from pydantic import BaseModel, Field


class ContactInfoView(BaseModel):
    email: str = Field(examples=['jdoe@gmail.com'])
    phone1: str = Field(examples=['+1 555-555-5555'])
    phone2: str = Field(examples=['+1 555-555-5555'])
