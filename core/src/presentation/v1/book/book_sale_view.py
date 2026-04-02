from pydantic import BaseModel, Field


class BookSaleView(BaseModel):
    """Book sale read view data"""
    saleable: bool = Field(examples=[True, False])
    price: float = Field(examples=[19.99, 29.99])
    discount: float = Field(examples=[0.0, 10.0, 20.0])
