from pydantic import Field, BaseModel

from src.application.customer.creator import CustomerCreatePayload

class MembershipUpdatePayload(BaseModel):
    active: bool = Field(default=True, examples=[True])


class CustomerUpdatePayload(CustomerCreatePayload):
    """
    Payload for updating an existing customer
    """
    membership: MembershipUpdatePayload
