from datetime import datetime

from pydantic import Field, BaseModel


class AuthorCreatePayload(BaseModel):
    """Payload for creating a new author."""
    name: str = Field(examples=['J.K. Rowling'])
    real_name: str = Field(alias="realName", examples=['Joanne Rowling'])
    genres: str = Field(examples=['Fantasy, Adventure'])
    biography: str = Field(examples=['J.K. Rowling is a British author, best known for writing the Harry Potter series.'])
    nationality: str = Field(examples=['British'])
    birth_date: datetime = Field(alias="birthDate", examples=['1965-07-31'])
    death_date: datetime | None = Field(alias="deathDate", default=None, examples=['2020-01-01'])
    photo_url: str = Field(alias="photoUrl", examples=['https://example.com/photos/jk_rowling.jpg'])
    website: str = Field(examples=['https://www.jkrowling.com/'])
