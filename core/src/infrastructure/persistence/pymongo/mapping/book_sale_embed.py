from pydantic import BaseModel


class BookSaleEmbed(BaseModel):
    saleable: bool
    price: float
    discount: float
