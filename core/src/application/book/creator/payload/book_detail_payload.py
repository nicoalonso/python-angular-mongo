from datetime import datetime

from pydantic import BaseModel, Field


class BookDetailPayload(BaseModel):
    """Payload for book detail."""
    edition: str = Field(examples=['First Edition'])
    isbn: str = Field(examples=['978-3161484100'])
    language: str = Field(examples=['English'])
    published_at: datetime = Field(alias="publishedAt", examples=['2020-01-01'])
    pages: int = Field(examples=[300])
