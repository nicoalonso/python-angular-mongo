from dataclasses import asdict
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_serializer

from src.domain.provider import Provider
from src.presentation.identity import Result, format_date
from src.presentation.v1.common import EnterpriseContactView, AddressView


class ProviderReadViewData(BaseModel):
    id: str = Field(examples=['123e4567-e89b-12d3-a456-426614174000'])
    name: str = Field(examples=['Amazon'])
    comercial_name: str = Field(serialization_alias='comercialName', examples=['Amazon Inc.'])
    contact: EnterpriseContactView
    address: AddressView
    vat_number: str = Field(serialization_alias='vatNumber', examples=['B123456789'])
    created_by: str = Field(serialization_alias='createdBy', examples=['user123'])
    created_at: datetime = Field(serialization_alias='createdAt', examples=['2024-01-01T12:00:00+01:00'])
    updated_by: Optional[str] = Field(serialization_alias='updatedBy', examples=['user456'])
    updated_at: Optional[datetime] = Field(serialization_alias='updatedAt', examples=['2024-01-02T12:00:00+01:00'])

    @field_serializer("created_at", "updated_at", when_used="unless-none")
    def serialize_date(self, value: datetime) -> Optional[str]:
        """Serialize datetime to ISO format string"""
        return format_date(value)  # pragma: no cover


class ProviderReadView(Result[ProviderReadViewData]):
    def __init__(self, provider: Provider):
        super().__init__(data=ProviderReadViewData(**asdict(provider)))
