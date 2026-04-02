from typing import Optional

from pydantic import Field

from src.domain.identity.list import ListQueryPayload


class AuthorQueryPayload(ListQueryPayload):
    """Author list filters"""
    name: Optional[str] = None
    real_name: Optional[str] = Field(default=None, alias='realName')
    nationality: Optional[str] = None
