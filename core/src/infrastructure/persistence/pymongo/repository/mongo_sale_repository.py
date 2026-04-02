from src.domain.identity import Collection
from src.domain.sale import Sale, SaleRepository, SaleCollection
from src.infrastructure.persistence.pymongo.mapping import SaleDocument
from .mongo_repository import MongoRepository


class MongoSaleRepository(MongoRepository[Sale], SaleRepository):
    """
    Repository for Sale entity using MongoDB as the data store.
    """

    def __init__(self, database):
        super().__init__(collection=database["sales"], model=SaleDocument)

    async def obtain_by_number(self, number: str) -> Sale | None:
        return await self._find_one_by({"number": number})

    async def obtain_by_customer(self, customer_id: str, limit: int | None = None) -> SaleCollection:
        items = await self._find_by({"customer.id": customer_id}, limit=limit)
        return Collection(items)
