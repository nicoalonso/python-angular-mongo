from pydantic import BaseModel


class ContactInfoEmbed(BaseModel):
    email: str
    phone1: str
    phone2: str
