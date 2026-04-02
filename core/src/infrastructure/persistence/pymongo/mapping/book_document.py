from datetime import datetime
from typing import Optional

from pydantic import Field, ConfigDict

from src.domain.author import AuthorDescriptor
from src.domain.book import Book, BookDetail, BookSale
from src.domain.editorial import EditorialDescriptor
from .book_detail_embed import BookDetailEmbed
from .book_sale_embed import BookSaleEmbed
from .editorial_embed import EditorialEmbed
from .mongo_document import MongoDocument
from .author_embed import AuthorEmbed


class BookDocument(MongoDocument[Book]):
    id: str = Field(alias="_id")
    title: str
    description: str
    author: AuthorEmbed
    editorial: EditorialEmbed
    detail: BookDetailEmbed
    sale: BookSaleEmbed
    stock: int
    created_by: str = Field(alias="createdBy")
    created_at: datetime = Field(alias="createdAt")
    updated_by: Optional[str] = Field(default=None, alias="updatedBy")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)

    def to_domain(self) -> Book:
        """
        Converts the BookDocument to a Book domain model.
        :return: (Book) domain model instance.
        """
        item = self.model_dump()
        item['author'] = AuthorDescriptor(**item.pop('author'))
        item['editorial'] = EditorialDescriptor(**item.pop('editorial'))
        item['detail'] = BookDetail(**item.pop('detail'))
        item['sale'] = BookSale(**item.pop('sale'))

        return Book(**item)
