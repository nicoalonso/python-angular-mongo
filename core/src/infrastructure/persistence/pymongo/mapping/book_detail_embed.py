from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class BookDetailEmbed(BaseModel):
    edition: str
    isbn: str
    language: str
    published_at: datetime = Field(alias="publishedAt")
    pages: int

    model_config = ConfigDict(populate_by_name=True)
