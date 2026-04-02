from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, Field

from src.domain.author import Author
from .mongo_document import MongoDocument


class AuthorDocument(MongoDocument[Author]):
    id: str = Field(alias="_id")
    name: str
    real_name: str = Field(alias="realName")
    genres: str
    biography: str
    nationality: str
    birth_date: datetime = Field(alias="birthDate")
    death_date: Optional[datetime] = Field(default=None, alias="deathDate")
    photo_url: str = Field(alias="photoUrl")
    website: str
    created_by: str = Field(alias="createdBy")
    created_at: datetime = Field(alias="createdAt")
    updated_by: Optional[str] = Field(default=None, alias="updatedBy")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)

    def to_domain(self) -> Author:
        """
        Converts the AuthorDocument to an Author domain model.
        :return: (Author) domain model instance.
        """
        return Author(**self.model_dump())
