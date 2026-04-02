from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class MembershipEmbed(BaseModel):
    number: str
    active: bool
    ended_at: Optional[datetime] = Field(default=None, alias="endedAt")

    model_config = ConfigDict(populate_by_name=True)
