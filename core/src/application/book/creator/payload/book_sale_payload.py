from pydantic import BaseModel, Field


class BookSalePayload(BaseModel):
    """Payload for book sale."""
    saleable: bool = Field(examples=[True])
    price: float = Field(examples=[19.99])
    discount: float = Field(examples=[10.0])
