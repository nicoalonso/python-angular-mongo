from pydantic import BaseModel, Field

from src.application.borrow.creator.payload.borrow_line_payload import BorrowLinePayload


class BorrowCreatePayload(BaseModel):
    """Payload for creating a borrow."""
    customer_id: str = Field(alias="customerId", examples=['123e4567-e89b-12d3-a456-426614174000'])
    lines: list[BorrowLinePayload]
