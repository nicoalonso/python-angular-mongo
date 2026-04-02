from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from src.application.borrow.reader import BorrowDecorator
from src.presentation.identity import Result
from src.presentation.v1.book import BookDescriptorView
from .borrow_list_view import BorrowListViewData


class BorrowLineViewData(BaseModel):
    id: str = Field(serialization_alias='lineId', examples=['123e4567-e89b-12d3-a456-426614174000'])
    book: BookDescriptorView
    returned: bool = Field(examples=[True])
    returned_date: Optional[datetime] = Field(serialization_alias='returnedDate', examples=['2024-01-10'])
    penalty: bool = Field(examples=[False])
    penalty_amount: float = Field(serialization_alias='penaltyAmount', examples=[15.0])


class BorrowReadViewData(BorrowListViewData):
    lines: list[BorrowLineViewData]


class BorrowReadView(Result[BorrowReadViewData]):
    def __init__(self, borrow: BorrowDecorator):
        item = borrow.to_dict()
        super().__init__(data=BorrowReadViewData(**item))
