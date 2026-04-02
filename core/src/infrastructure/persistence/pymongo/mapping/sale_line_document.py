from pydantic import Field, ConfigDict

from src.domain.book import BookDescriptor
from src.domain.sale import SaleLine
from .mongo_document import MongoDocument
from .book_embed import BookEmbed


class SaleLineDocument(MongoDocument[SaleLine]):
    """
    MongoDB document representation of the SaleLine entity.
    """
    id: str = Field(alias="_id")
    sale: str
    book: BookEmbed
    quantity: int
    price: float
    discount: float
    total: float

    model_config = ConfigDict(populate_by_name=True)

    def to_domain(self) -> SaleLine:
        """
        Converts the SaleLineDocument to a SaleLine domain model.
        :return: (SaleLine) domain model instance.
        """
        item = self.model_dump()
        item['book'] = BookDescriptor(**item.pop('book'))

        return SaleLine(**item)
