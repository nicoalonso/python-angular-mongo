from pydantic import Field, ConfigDict

from src.domain.book import BookDescriptor
from src.domain.purchase import PurchaseLine
from .mongo_document import MongoDocument
from .book_embed import BookEmbed


class PurchaseLineDocument(MongoDocument[PurchaseLine]):
    """
    MongoDB document representation of the PurchaseLine entity.
    """
    id: str = Field(alias="_id")
    purchase: str
    book: BookEmbed
    quantity: int
    unit_price: float = Field(alias="unitPrice")
    discount_percentage: float = Field(alias="discountPercentage")
    total: float

    model_config = ConfigDict(populate_by_name=True)

    def to_domain(self) -> PurchaseLine:
        """
        Converts the PurchaseLineDocument to a PurchaseLine domain model.
        :return: (PurchaseLine) domain model instance.
        """
        item = self.model_dump()
        item['book'] = BookDescriptor(**item.pop('book'))

        return PurchaseLine(**item)
