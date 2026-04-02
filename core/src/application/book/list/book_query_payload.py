from typing import Optional

from pydantic import Field

from src.domain.identity.list import ListQueryPayload


class BookQueryPayload(ListQueryPayload):
    """Book list filters"""
    title: Optional[str] = None
    author: Optional[str] = None
    editorial: Optional[str] = None
    isbn: Optional[str] = None
    language: Optional[str] = None
    from_published_date: Optional[str] = Field(default=None, alias='fromPublishedDate')
    to_published_date: Optional[str] = Field(default=None, alias='toPublishedDate')
    from_price: Optional[float] = Field(default=None, alias='fromPrice')
    to_price: Optional[float] = Field(default=None, alias='toPrice')
    saleable: Optional[bool] = None
