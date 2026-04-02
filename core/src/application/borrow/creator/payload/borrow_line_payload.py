from pydantic import BaseModel, Field


class BorrowLinePayload(BaseModel):
    """Payload for creating a borrow line."""
    line_id: str = Field(default='', alias="lineId", examples=['123e4567-e89b-12d3-a456-426614174000'])
    book_id: str = Field(alias="bookId", examples=['123e4567-e89b-12d3-a456-426614174000'])
    returned: bool = False
