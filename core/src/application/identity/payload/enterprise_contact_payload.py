from pydantic import BaseModel, Field

from .validators import OptionalUrl, OptionalEmail


class EnterpriseContactPayload(BaseModel):
    email: OptionalEmail
    website: OptionalUrl
    phone1: str = Field(examples=['+1 123 456 7890'])
    phone2: str = Field(examples=['+1 123 456 7890'])
