from typing import Optional

from pydantic import Field

from src.domain.identity.list import ListQueryPayload


class EditorialQueryPayload(ListQueryPayload):
    """Editorial list filters"""
    name: Optional[str] = None
    comercial_name: Optional[str] = Field(default=None, alias='comercialName')
    website: Optional[str] = None
