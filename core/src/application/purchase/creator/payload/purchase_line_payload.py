from pydantic import BaseModel, Field


class PurchaseLinePayload(BaseModel):
    """Payload for creating a purchase line."""
    line_id: str = Field(default='', alias="lineId", examples=['123e4567-e89b-12d3-a456-426614174000'])
    book_id: str = Field(alias="bookId", examples=['123e4567-e89b-12d3-a456-426614174000'])
    quantity: int = Field(examples=[1, 2, 3])
    unit_price: float = Field(alias="unitPrice", examples=[9.99, 19.99])
    discount_percentage: float = Field(alias="discountPercentage", examples=[0.0, 10.0, 20.0])
    total: float = Field(examples=[9.99, 17.99, 15.99])
