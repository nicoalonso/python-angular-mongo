from datetime import datetime
from typing import Optional

from pydantic import Field, ConfigDict

from src.domain.borrow import Borrow
from src.domain.customer import CustomerDescriptor
from .customer_embed import CustomerEmbed
from .mongo_document import MongoDocument


class BorrowDocument(MongoDocument[Borrow]):
    """
    MongoDB document representation of the Borrow entity.
    """
    id: str = Field(alias="_id")
    customer: CustomerEmbed
    number: str
    borrow_date: datetime = Field(alias="borrowDate")
    total_books: int = Field(alias="totalBooks")
    due_date: datetime = Field(alias="dueDate")
    total_returned_books: int = Field(alias="totalReturnedBooks")
    returned: bool
    returned_date: Optional[datetime] = Field(default=None, alias="returnedDate")
    penalty: bool
    penalty_amount: float = Field(alias="penaltyAmount")
    created_by: str = Field(alias="createdBy")
    created_at: datetime = Field(alias="createdAt")
    updated_by: Optional[str] = Field(default=None, alias="updatedBy")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)

    def to_domain(self) -> Borrow:
        """
        Converts the BorrowDocument to a Borrow domain model.
        :return: (Borrow) domain model instance.
        """
        item = self.model_dump()
        item['customer'] = CustomerDescriptor(**item.pop('customer'))

        return Borrow(**item)
