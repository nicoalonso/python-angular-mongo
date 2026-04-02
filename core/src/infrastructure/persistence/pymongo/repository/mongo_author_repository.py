from pymongo.asynchronous.database import AsyncDatabase

from src.domain.author import AuthorRepository, Author
from src.infrastructure.persistence.pymongo.mapping.author_document import AuthorDocument
from .mongo_repository import MongoRepository


class MongoAuthorRepository(MongoRepository[Author], AuthorRepository):
    """
    Repository for Author entity using MongoDB as the data store.
    """

    def __init__(self, database: AsyncDatabase):
        super().__init__(collection=database["authors"], model=AuthorDocument)

    async def obtain_by_name(self, name: str) -> Author:
        return await self._find_one_by({"name": name})
