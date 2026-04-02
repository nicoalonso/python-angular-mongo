from pydantic import BaseModel, Field

from src.application.book.creator.payload import BookDetailPayload, BookSalePayload


class BookCreatePayload(BaseModel):
    """Payload for creating a book."""
    title: str = Field(examples=['The Great Gatsby'])
    description: str = Field(examples=['A novel about the American dream.'])
    author_id: str = Field(alias="authorId", examples=['123e4567-e89b-12d3-a456-426614174000'])
    editorial_id: str = Field(alias="editorialId", examples=['123e4567-e89b-12d3-a456-426614174000'])
    detail: BookDetailPayload
    sale: BookSalePayload
