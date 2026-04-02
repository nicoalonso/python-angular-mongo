from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_serializer

from src.presentation.identity import format_date


class MembershipView(BaseModel):
    number: str = Field(examples=['SN-00225'])
    active: bool = Field(examples=[True])
    ended_at: Optional[datetime] = Field(default=None, serialization_alias='endedAt', examples=['2024-12-31'])

    @field_serializer("ended_at", when_used="unless-none")
    def serialize_date(self, value: datetime) -> Optional[str]:
        """Serialize datetime to ISO format string"""
        return format_date(value)  # pragma: no cover
