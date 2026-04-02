from datetime import datetime
from typing import Optional

from pydantic import Field, ConfigDict

from src.domain.summary import Summary, SummaryState, SummaryType
from src.infrastructure.persistence.pymongo.mapping import MongoDocument


class SummaryDocument(MongoDocument[Summary]):
    """
    MongoDB document representation of the Summary entity.
    """
    id: str = Field(alias="_id")
    url: str
    type: str
    state: str
    reason: str
    content: str
    created_by: str = Field(alias="createdBy")
    created_at: datetime = Field(alias="createdAt")
    updated_by: Optional[str] = Field(default=None, alias="updatedBy")
    updated_at: Optional[datetime] = Field(default=None, alias="updatedAt")

    model_config = ConfigDict(populate_by_name=True)

    def to_domain(self) -> Summary:
        """
        Converts the SummaryDocument to a Summary domain model.
        :return: (Summary) domain model instance.
        """
        item = self.model_dump()
        item['type'] = SummaryType.try_from(item.pop('type'))
        item['state'] = SummaryState.try_from(item.pop('state'))

        return Summary(**item)
