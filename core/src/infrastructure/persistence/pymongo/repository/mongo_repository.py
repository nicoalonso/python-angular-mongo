import logging
from dataclasses import asdict
from typing import TypeVar, Mapping, Any, Optional

from pydantic import ValidationError
from pymongo.asynchronous.collection import AsyncCollection

from src.domain.identity import ListRepository, Collection
from src.domain.identity.list import ListQuery, ListResult, FilterType, FilterField, Pagination
from src.infrastructure.persistence.pymongo.mapping import MongoDocument


T = TypeVar('T')


class MongoRepository(ListRepository[T]):
    """
    Base repository class for MongoDB operations. Provides common methods for interacting with a MongoDB collection.

    Attributes:
        collection (AsyncCollection): The MongoDB collection to operate on.
        model (type MongoDocument[T]): The Pydantic model representing the MongoDB document structure.
    """
    def __init__(self, collection: AsyncCollection, model: type[MongoDocument[T]]):
        self.collection = collection
        self.model: type[MongoDocument[T]] = model

    async def obtain_by_id(self, entity_id: str) -> T | None:
        """Fetches a single entity by its unique identifier."""
        return await self._find_one_by({"_id": entity_id})

    async def save(self, element: T) -> None:
        """Saves an entity to the MongoDB collection. If the entity already exists, it will be updated."""
        logger = logging.getLogger('uvicorn.error')

        try:
            item = self._prime(element)
            await self.collection.replace_one({"_id": item["_id"]}, item, upsert=True)

        except ValidationError as e:
            logger.error("Validation error while parsing: %s", str(e), exc_info=e)
            raise Exception("Failed to save the entity due to validation errors.")
        except Exception as e:
            logger.error("Error while saving entity: %s", str(e), exc_info=e)
            raise Exception("Failed to save the entity due to an unexpected error.")

    def _prime(self, element: T) -> dict:
        """Converts a domain entity into a MongoDB document using the Pydantic model."""
        # noinspection PyArgumentList
        return self.model(**asdict(element)).to_db()

    async def remove(self, id_: str) -> None:
        """Removes an entity from the MongoDB collection by its unique identifier."""
        await self.collection.delete_one({"_id": id_})

    async def obtain_by_query(self, query: ListQuery) -> ListResult[T]:
        """Fetches entities matching the provided query parameters."""
        where = self._make_where(query)
        sort = self._make_sort(query)

        count = await self.collection.count_documents(where)

        items = await (self.collection
                       .find(where, sort=sort, limit=query.limit, skip=query.offset)
                       .to_list(length=None))

        collection = Collection([self._hydrate(item) for item in items])
        pagination = Pagination(count, query.page, query.limit)

        return ListResult(collection, pagination)

    def _make_where(self, query: ListQuery) -> dict:
        """Converts a ListQuery into a MongoDB query dictionary."""
        where = {}
        if not query.has_filters():
            return where

        for filter_ in query.filters:
            if not filter_.has_value():
                continue

            value = None
            match filter_.type_:
                case FilterType.Wildcard | FilterType.Fuzzy:
                    value = {"$regex": filter_.value, "$options": "i"}
                case FilterType.Range:
                    value = self._range_filter(filter_)
                case FilterType.In:
                    value = {"$in": filter_.value}
                case FilterType.All:
                    value = {"$all": filter_.value}
                case FilterType.Exists:
                    value = {"$exists": filter_.value}
                case _:
                    value = filter_.value

            if value is not None:
                where[filter_.name] = value

        return where

    @staticmethod
    def _range_filter(filter_: FilterField) -> Optional[dict]:
        if not filter_.is_range():
            return None

        range_query = {}
        if filter_.value.has_from():
            range_query["$gte"] = filter_.value.from_
        if filter_.value.has_to():
            range_query["$lte"] = filter_.value.to

        return range_query

    @staticmethod
    def _make_sort(query: ListQuery) -> dict[str, int]:
        """Converts a ListQuery's sorting parameters into a MongoDB sort list."""
        sort = {}
        if not query.has_sort():
            return sort

        for sort_element in query.sort:
            sort[sort_element.name] = 1 if sort_element.is_ascending() else -1

        return sort

    async def _find_one_by(self, query: dict) -> T | None:
        """Fetches a single entity matching the provided query."""
        item = await self.collection.find_one(query)
        if item is None:
            return None

        return self._hydrate(item)

    async def _find_by(self, query: dict, limit: int | None = None) -> list[T]:
        """Fetches multiple entities matching the provided query."""
        kwargs = {}
        if limit is not None:
            kwargs['limit'] = limit

        cursor = self.collection.find(query, **kwargs)
        items = await cursor.to_list(length=None)
        return [self._hydrate(item) for item in items]

    def _hydrate(self, item: Mapping[str, Any]) -> T:
        """Converts a MongoDB document into a domain entity using the Pydantic model."""
        try:
            # noinspection PyArgumentList
            document = self.model(**item)
        except ValidationError as e:
            logger = logging.getLogger('uvicorn.error')
            logger.error("Validation error while parsing: %s", str(e), exc_info=e)
            return None

        return document.to_domain()
