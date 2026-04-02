from dataclasses import asdict

from pymongo.asynchronous.database import AsyncDatabase

from src.domain.sequence import SequenceNumber, SequenceNumberRepository, SequenceType
from src.infrastructure.persistence.pymongo.mapping import SequenceNumberDocument
from .mongo_repository import MongoRepository


class MongoSequenceNumberRepository(MongoRepository[SequenceNumber], SequenceNumberRepository):
    """
    Repository for SequenceNumber entity using MongoDB as the data store.
    """

    def __init__(self, database: AsyncDatabase):
        super().__init__(collection=database["sequences"], model=SequenceNumberDocument)

    async def obtain_by_type(self, type_: SequenceType) -> SequenceNumber:
        number = await self._find_one_by({"type": type_.value})
        if number is None:
            number = SequenceNumber.create(type_)
        else:
            number.next()

        return number

    async def next_number(self, type_: SequenceType) -> SequenceNumber:
        number = await self._find_one_by({"type": type_.value})
        if number is None:
            number = SequenceNumber.create(type_)
        else:
            number.next()

        await self.save(number)
        return number

    def _prime(self, element: SequenceNumber) -> dict:
        item = asdict(element)
        item["type"] = element.type.value
        # noinspection PyArgumentList
        return self.model(**item).to_db()
