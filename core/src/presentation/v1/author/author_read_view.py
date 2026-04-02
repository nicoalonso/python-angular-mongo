from dataclasses import asdict
from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field, field_serializer

from src.domain.author import Author
from src.presentation.identity import Result, format_date, format_short_date


class AuthorReadViewData(BaseModel):
    id: str = Field(examples=['123e4567-e89b-12d3-a456-426614174000'])
    name: str = Field(examples=['J.K. Rowling'])
    real_name: str = Field(serialization_alias='realName', examples=['Joanne Rowling'])
    genres: str = Field(examples=['Fantasy, Adventure'])
    biography: str = Field(examples=['J.K. Rowling is a British author, best known for writing the Harry Potter series.'])
    nationality: str = Field(examples=['British'])
    birth_date: datetime = Field(serialization_alias='birthDate', examples=['1965-07-31'])
    death_date: Optional[datetime] = Field(serialization_alias='deathDate', examples=['2020-01-01'])
    photo_url: str = Field(serialization_alias='photoUrl', examples=['https://example.com/photos/jk_rowling.jpg'])
    website: str = Field(examples=['https://www.jkrowling.com/'])
    created_by: str = Field(serialization_alias='createdBy', examples=['admin'])
    created_at: datetime = Field(serialization_alias='createdAt', examples=['2026-03-02T12:15:10+01:00'])
    updated_by: Optional[str] = Field(serialization_alias='updatedBy', examples=['editor'])
    updated_at: Optional[datetime] = Field(serialization_alias='updatedAt', examples=['2026-03-10T09:30:00+01:00'])

    @field_serializer("birth_date", "death_date", when_used="unless-none")
    def serialize_short_date(self, value: datetime) -> Optional[str]:
        """Serialize datetime to ISO format string"""
        return format_short_date(value)  # pragma: no cover

    @field_serializer("created_at", "updated_at", when_used="unless-none")
    def serialize_date(self, value: datetime) -> Optional[str]:
        """Serialize datetime to ISO format string"""
        return format_date(value)  # pragma: no cover


class AuthorReadView(Result[AuthorReadViewData]):
    def __init__(self, author: Author):
        super().__init__(data=AuthorReadViewData(**asdict(author)))
