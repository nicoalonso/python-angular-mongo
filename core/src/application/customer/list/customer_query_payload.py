from typing import Optional

from pydantic import Field

from src.domain.identity.list import ListQueryPayload


class CustomerQueryPayload(ListQueryPayload):
    """Customer list filters"""
    name: Optional[str] = None
    surname: Optional[str] = None
    number: Optional[str] = None
    active: Optional[bool] = None
    city: Optional[str] = None
    vat_number: Optional[str] = Field(default=None, alias='vatNumber')
