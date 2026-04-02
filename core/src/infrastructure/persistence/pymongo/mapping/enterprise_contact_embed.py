from pydantic import BaseModel


class EnterpriseContactEmbed(BaseModel):
    email: str
    website: str
    phone1: str
    phone2: str
