from typing import Optional

from pydantic import BaseModel, Field


class ListQueryPayload(BaseModel):
    """Common list filters"""
    id: Optional[str] = None
    created_by: Optional[str] = Field(default=None, alias='createdBy')
    from_created_at: Optional[str] = Field(default=None, alias='fromCreatedAt')
    to_created_at: Optional[str] = Field(default=None, alias='toCreatedAt')
    updated_by: Optional[str] = Field(default=None, alias='updatedBy')
    from_updated_at: Optional[str] = Field(default=None, alias='fromUpdatedAt')
    to_updated_at: Optional[str] = Field(default=None, alias='toUpdatedAt')
    page: Optional[int] = Field(default=None, ge=1)
    limit: Optional[int] = Field(default=None, ge=1)
    sort: Optional[str] = None
