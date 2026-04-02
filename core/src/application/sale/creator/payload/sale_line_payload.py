from pydantic import BaseModel, Field


class SaleLinePayload(BaseModel):
    """Payload for creating a sale line."""
    line_id: str = Field(default='', alias="lineId", examples=['123e4567-e89b-12d3-a456-426614174000'])
    book_id: str = Field(alias="bookId", examples=['123e4567-e89b-12d3-a456-426614174000'])
    quantity: int = Field(examples=[1])
    price: float = Field(examples=[19.99])
    discount: float = Field(examples=[0.0])
    total: float = Field(examples=[19.99])
