from pymongo.asynchronous.database import AsyncDatabase

from src.domain.provider import Provider, ProviderRepository
from src.infrastructure.persistence.pymongo.mapping import ProviderDocument
from .mongo_repository import MongoRepository


class MongoProviderRepository(MongoRepository[Provider], ProviderRepository):
    """
    Repository for Provider entity using MongoDB as the data store.
    """

    def __init__(self, database: AsyncDatabase):
        super().__init__(collection=database["providers"], model=ProviderDocument)

    async def obtain_by_name(self, name: str) -> Provider | None:
        return await self._find_one_by({"name": name})
