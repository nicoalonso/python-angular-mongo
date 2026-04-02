from abc import ABC, abstractmethod
from typing import TypeVar, Optional, Any, cast

from src.domain.identity import ListRepository, Collection
from src.domain.identity.list import ListQuery, ListResult, Pagination
from tests.fixtures import Ref

T = TypeVar('T')


class EntityRepositoryStub(ListRepository[T], ABC):
    """A stub for the EntityRepository interface used in tests."""
    def __init__(self):
        self._repository_data: dict[Ref, T] = {}
        self.list: Collection[T] = Collection()
        self.read: Optional[T] = None
        self.stored: Optional[T] = None
        self.removed: Optional[str] = None
        # query strings and errors
        self.query: Optional[ListQuery] = None
        self.query_filter: Optional[Any] = None
        self._exception: Optional[Exception] = None

        self.make_fixtures()

    @abstractmethod
    def make_fixtures(self) -> None: ...

    def add_fixture(self, ref: Ref, entity: T) -> None:
        self._repository_data[ref] = entity

    async def obtain_by_id(self, entity_id: str) -> T | None:
        self.query_filter = entity_id
        self._throw_error()
        return self.read

    async def obtain_by_query(self, query: ListQuery) -> ListResult[T]:
        self.query = query
        self._throw_error()

        pagination = Pagination(
            self.list.count(),
            query.page,
            query.limit,
        )
        result = ListResult(
            items=self.list,
            pagination=pagination,
        )
        return result

    async def save(self, element: T) -> None:
        self._throw_error()
        self.stored = element

    async def remove(self, id_: str) -> None:
        self._throw_error()
        self.removed = id_

    def attach_all(self) -> Collection[T]:
        data = list(self._repository_data.values())
        self.list = Collection(data)
        return self.list

    def attach(self, ref: Ref) -> Optional[T]:
        item: Optional[T] = self.get(ref)
        if item is not None:
            self.list.add(item)

        return item

    def manual_attach(self, item: T) -> None:
        self.list.add(item)

    def put(self, ref: Ref) -> Optional[T]:
        item: Optional[T] = self.get(ref)
        if item is not None:
            self.read = item

        return item

    def manual_put(self, item: T) -> None:
        self.read = item

    def clear(self):
        self._repository_data.clear()
        self.list.clear()
        self.read = None
        self.stored = None
        self.removed = None
        self.query = None
        self.query_filter = None
        self._exception = None

    def get(self, ref: Ref) -> Optional[T]:
        return self._repository_data.get(ref)

    def error(self, exception: Exception | str) -> None:
        if isinstance(exception, str):
            exception = Exception(exception)
        self._exception = cast(Exception, exception)

    def _throw_error(self):
        if self._exception:
            raise self._exception
