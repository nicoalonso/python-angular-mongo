from abc import ABC, abstractmethod
from typing import TypeVar

from .list import ListQuery, ListResult
from .stored_repository import StoredRepository


T = TypeVar('T')


class ListRepository(StoredRepository[T], ABC):
    """
    Abstract base class for List repository.
    Defines the interface for obtaining entities from a data store.
    """
    @abstractmethod
    async def obtain_by_id(self, entity_id: str) -> T | None: ...

    @abstractmethod
    async def obtain_by_query(self, query: ListQuery) -> ListResult[T]: ...
