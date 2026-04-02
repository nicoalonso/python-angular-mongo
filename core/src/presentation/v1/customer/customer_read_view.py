from dataclasses import asdict
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_serializer

from src.domain.customer import Customer
from src.presentation.identity import Result, format_date
from src.presentation.v1.common import AddressView
from .contact_info_view import ContactInfoView
from .membership_view import MembershipView


class CustomerReadViewData(BaseModel):
    id: str = Field(examples=['123e4567-e89b-12d3-a456-426614174000'])
    name: str = Field(examples=['John'])
    surname: str = Field(examples=['Doe'])
    membership: MembershipView
    contact: ContactInfoView
    address: AddressView
    vat_number: str = Field(serialization_alias='vatNumber', examples=['123456789A'])
    created_by: str = Field(serialization_alias='createdBy', examples=['admin'])
    created_at: datetime = Field(serialization_alias='createdAt', examples=['2024-01-01T12:00:00+01:00'])
    updated_by: Optional[str] = Field(serialization_alias='updatedBy', examples=['admin'])
    updated_at: Optional[datetime] = Field(serialization_alias='updatedAt', examples=['2024-01-02T12:00:00+01:00'])

    @field_serializer("created_at", "updated_at", when_used="unless-none")
    def serialize_date(self, value: datetime) -> Optional[str]:
        """Serialize datetime to ISO format string"""
        return format_date(value)  # pragma: no cover


class CustomerReadView(Result[CustomerReadViewData]):
    def __init__(self, customer: Customer):
        super().__init__(data=CustomerReadViewData(**asdict(customer)))
