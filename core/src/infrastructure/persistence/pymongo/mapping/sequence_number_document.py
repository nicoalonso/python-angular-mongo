from pydantic import Field, ConfigDict

from src.domain.sequence import SequenceNumber, SequenceType
from src.infrastructure.persistence.pymongo.mapping import MongoDocument


class SequenceNumberDocument(MongoDocument):
    id: str = Field(alias="_id")
    type: str
    prefix: str
    number: int

    model_config = ConfigDict(populate_by_name=True)

    def to_domain(self) -> SequenceNumber:
        """
        Converts the CustomerDocument to a Customer domain model.
        :return: (Customer) domain model instance.
        """
        item = self.model_dump()
        item['type'] = SequenceType.try_from(item.pop('type'))

        return SequenceNumber(**item)
