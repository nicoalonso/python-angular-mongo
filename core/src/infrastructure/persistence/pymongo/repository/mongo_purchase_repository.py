from pymongo.asynchronous.database import AsyncDatabase

from src.domain.identity import Collection
from src.domain.purchase import Purchase, PurchaseRepository
from src.domain.purchase.purchase import PurchaseCollection
from src.infrastructure.persistence.pymongo.mapping import PurchaseDocument
from .mongo_repository import MongoRepository


class MongoPurchaseRepository(MongoRepository[Purchase], PurchaseRepository):
    """
    Repository for Purchase entity using MongoDB as the data store.
    """

    def __init__(self, database: AsyncDatabase):
        super().__init__(collection=database["purchases"], model=PurchaseDocument)

    async def obtain_by_provider_and_number(self, provider_id: str, invoice_number: str) -> Purchase | None:
        return await self._find_one_by({
            "provider.id": provider_id,
            "invoice.number": invoice_number
        })

    async def obtain_by_provider(self, provider_id: str, limit: int | None = None) -> PurchaseCollection:
        items = await self._find_by({"provider.id": provider_id}, limit=limit)
        return Collection(items)
