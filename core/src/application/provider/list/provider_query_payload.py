from typing import Optional

from pydantic import Field

from src.domain.identity.list import ListQueryPayload


class ProviderQueryPayload(ListQueryPayload):
    """Provider list filters"""
    name: Optional[str] = None
    comercial_name: Optional[str] = Field(default=None, alias='comercialName')
    vat_number: Optional[str] = Field(default=None, alias='vatNumber')
    website: Optional[str] = None
