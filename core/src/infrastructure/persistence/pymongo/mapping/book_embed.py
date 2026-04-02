from pydantic import BaseModel


class BookEmbed(BaseModel):
    id: str
    title: str
    isbn: str
