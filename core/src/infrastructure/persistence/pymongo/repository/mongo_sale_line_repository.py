from src.domain.identity import Collection
from src.domain.sale import SaleLine, SaleLineRepository, SaleLineCollection
from src.infrastructure.persistence.pymongo.mapping import SaleLineDocument
from .mongo_repository import MongoRepository


class MongoSaleLineRepository(MongoRepository[SaleLine], SaleLineRepository):
    """
    Repository for SaleLine entity using MongoDB as the data store.
    """

    def __init__(self, database):
        super().__init__(collection=database["saleLines"], model=SaleLineDocument)

    async def obtain_by_sale(self, sale_id: str) -> SaleLineCollection:
        items = await self._find_by({"sale": sale_id})
        return Collection(items)

    async def obtain_by_book(self, book_id: str, limit: int | None = None) -> SaleLineCollection:
        items = await self._find_by({"book.id": book_id}, limit=limit)
        return Collection(items)
