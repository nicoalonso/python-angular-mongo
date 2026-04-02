from pydantic import BaseModel, Field

from src.application.purchase.reader import PurchaseDecorator
from src.presentation.identity import Result
from src.presentation.v1.book import BookDescriptorView
from .purchase_list_view import PurchaseListViewData


class PurchaseLineViewData(BaseModel):
    id: str = Field(serialization_alias='lineId', examples=['123e4567-e89b-12d3-a456-426614174000'])
    book: BookDescriptorView
    quantity: int = Field(examples=[1, 2, 3])
    unit_price: float = Field(serialization_alias='unitPrice', examples=[9.99, 19.99])
    discount_percentage: float = Field(serialization_alias='discountPercentage', examples=[0.0, 10.0, 20.0])
    total: float = Field(serialization_alias='total', examples=[9.99, 17.99, 15.99])


class PurchaseReadViewData(PurchaseListViewData):
    lines: list[PurchaseLineViewData]


class PurchaseReadView(Result[PurchaseReadViewData]):
    def __init__(self, purchase: PurchaseDecorator):
        item = purchase.to_dict()
        super().__init__(data=PurchaseReadViewData(**item))
