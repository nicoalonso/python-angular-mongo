from typing import Optional

from pydantic import Field

from src.domain.identity.list import ListQueryPayload


class SaleQueryPayload(ListQueryPayload):
    """Sale list filters"""
    customer: Optional[str] = None
    from_date: Optional[str] = Field(default=None, alias='fromDate')
    to_date: Optional[str] = Field(default=None, alias='toDate')
    number: Optional[str] = None
