from abc import ABC, abstractmethod
from typing import TypeVar, Generic


T = TypeVar('T')


class StoredRepository(Generic[T], ABC):
    """
    Interface for repositories that support persistence
    """
    @abstractmethod
    async def save(self, element: T) -> None: ...

    @abstractmethod
    async def remove(self, id_: str) -> None: ...
