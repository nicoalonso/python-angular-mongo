from pymongo.asynchronous.database import AsyncDatabase

from src.domain.book import Book, BookCollection
from src.domain.book.book_repository import BookRepository
from src.domain.identity import Collection
from src.infrastructure.persistence.pymongo.mapping import BookDocument
from src.infrastructure.persistence.pymongo.repository.mongo_repository import MongoRepository


class MongoBookRepository(MongoRepository[Book], BookRepository):
    """
    Repository for Book entity using MongoDB as the data store.
    """

    def __init__(self, database: AsyncDatabase):
        super().__init__(collection=database["books"], model=BookDocument)

    async def obtain_by_title(self, title: str) -> Book | None:
        return await self._find_one_by({"title": title})

    async def obtain_by_author(self, author_id: str, limit: int | None = None) -> BookCollection:
        items = await self._find_by({"author.id": author_id}, limit=limit)
        return Collection(items)

    async def obtain_by_editorial(self, editorial_id: str, limit: int | None = None) -> BookCollection:
        items =  await self._find_by({"editorial.id": editorial_id}, limit=limit)
        return Collection(items)
