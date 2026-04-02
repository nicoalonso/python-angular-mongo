from pydantic import BaseModel, Field

from src.application.identity.payload import OptionalEmail


class ContactPayload(BaseModel):
    """Payload for contact information."""
    email: OptionalEmail
    phone1: str = Field(examples=['+1234567890'])
    phone2: str = Field(examples=['+0987654321'])
