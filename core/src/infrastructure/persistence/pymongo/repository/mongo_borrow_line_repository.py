from src.domain.borrow import BorrowLine, BorrowLineRepository, BorrowLineCollection
from src.domain.identity import Collection
from src.infrastructure.persistence.pymongo.mapping import BorrowLineDocument
from .mongo_repository import MongoRepository


class MongoBorrowLineRepository(MongoRepository[BorrowLine], BorrowLineRepository):
    """
    Repository for BorrowLine entity using MongoDB as the data store.
    """

    def __init__(self, database):
        super().__init__(collection=database["borrowLines"], model=BorrowLineDocument)

    async def obtain_by_borrow(self, borrow_id: str) -> BorrowLineCollection:
        items = await self._find_by({"borrow": borrow_id})
        return Collection(items)

    async def obtain_by_book(self, book_id: str, limit: int | None = None) -> BorrowLineCollection:
        items = await self._find_by({"book.id": book_id}, limit=limit)
        return Collection(items)

    async def obtain_active_by_book(self, book_id: str) -> BorrowLineCollection:
        items = await self._find_by({"borrow": book_id, "returned": False})
        return Collection(items)
