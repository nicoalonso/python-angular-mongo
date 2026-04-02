from datetime import datetime
from typing import Optional

from pydantic import Field, ConfigDict

from src.domain.book import BookDescriptor
from src.domain.borrow import BorrowLine
from .book_embed import BookEmbed
from .mongo_document import MongoDocument


class BorrowLineDocument(MongoDocument[BorrowLine]):
    """
    MongoDB document representation of the BorrowLine entity.
    """
    id: str = Field(alias="_id")
    borrow: str
    book: BookEmbed
    returned: bool
    returned_date: Optional[datetime] = Field(default=None, alias="returnedDate")
    penalty: bool
    penalty_amount: float = Field(alias="penaltyAmount")

    model_config = ConfigDict(populate_by_name=True)

    def to_domain(self) -> BorrowLine:
        """
        Converts the SaleLineDocument to a SaleLine domain model.
        :return: (SaleLine) domain model instance.
        """
        item = self.model_dump()
        item['book'] = BookDescriptor(**item.pop('book'))

        return BorrowLine(**item)
