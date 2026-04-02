from pymongo.asynchronous.database import AsyncDatabase

from src.domain.editorial import Editorial, EditorialRepository
from src.infrastructure.persistence.pymongo.mapping import EditorialDocument
from .mongo_repository import MongoRepository


class MongoEditorialRepository(MongoRepository[Editorial], EditorialRepository):
    """
    Repository for Editorial entity using MongoDB as the data store.
    """

    def __init__(self, database: AsyncDatabase):
        super().__init__(collection=database["editorials"], model=EditorialDocument)

    async def obtain_by_name(self, name: str) -> Editorial | None:
        return await self._find_one_by({"name": name})
