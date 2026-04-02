from src.domain.identity import Collection
from src.domain.purchase import PurchaseLineRepository, PurchaseLine, PurchaseLineCollection
from src.infrastructure.persistence.pymongo.mapping import PurchaseLineDocument
from src.infrastructure.persistence.pymongo.repository.mongo_repository import MongoRepository


class MongoPurchaseLineRepository(MongoRepository[PurchaseLine], PurchaseLineRepository):
    """
    Repository for PurchaseLine entity using MongoDB as the data store.
    """

    def __init__(self, database):
        super().__init__(collection=database["purchaseLines"], model=PurchaseLineDocument)

    async def obtain_by_purchase(self, purchase_id: str) -> PurchaseLineCollection:
        items = await self._find_by({"purchase": purchase_id})
        return Collection(items)

    async def obtain_by_book(self, book_id: str, limit: int | None = None) -> PurchaseLineCollection:
        items = await self._find_by({"book.id": book_id}, limit=limit)
        return Collection(items)
