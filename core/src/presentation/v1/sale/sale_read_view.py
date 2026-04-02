from pydantic import BaseModel, Field

from src.application.sale.reader import SaleDecorator
from src.presentation.identity import Result
from src.presentation.v1.book import BookDescriptorView
from .sale_list_view import SaleListViewData


class SaleLineViewData(BaseModel):
    id: str = Field(serialization_alias='lineId', examples=['123e4567-e89b-12d3-a456-426614174000'])
    book: BookDescriptorView
    quantity: int = Field(examples=[2])
    price: float = Field(examples=[19.99])
    discount: float = Field(examples=[0.1])
    total: float = Field(examples=[17.99])


class SaleReadViewData(SaleListViewData):
    lines: list[SaleLineViewData]


class SaleReadView(Result[SaleReadViewData]):
    def __init__(self, sale: SaleDecorator):
        item = sale.to_dict()
        super().__init__(data=SaleReadViewData(**item))
