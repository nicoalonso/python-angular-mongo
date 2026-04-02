from datetime import datetime

from src.domain.borrow import Borrow, BorrowRepository
from src.domain.borrow.borrow import BorrowCollection
from src.domain.identity import Collection
from src.infrastructure.persistence.pymongo.mapping import BorrowDocument
from .mongo_repository import MongoRepository


class MongoBorrowRepository(MongoRepository[Borrow], BorrowRepository):
    """
    Repository for Borrow entity using MongoDB as the data store.
    """

    def __init__(self, database):
        super().__init__(collection=database["borrows"], model=BorrowDocument)

    async def obtain_by_number(self, number: str) -> Borrow | None:
        return await self._find_one_by({"number": number})

    async def obtain_by_customer(self, customer_id: str, limit: int | None = None) -> BorrowCollection:
        items = await self._find_by({"customer.id": customer_id}, limit=limit)
        return Collection(items)

    async def obtain_by_overdue(self) -> BorrowCollection:
        query = {
            'returned': False,
            'dueDate': { '$lt': datetime.now() }
        }

        items = await self._find_by(query)
        return Collection(items)
