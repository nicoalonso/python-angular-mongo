from abc import ABC, abstractmethod

from src.domain.identity import ListRepository
from .author import Author


class AuthorRepository(ListRepository[Author], ABC):
    """
    Abstract base class for Author repository.
    Defines the interface for obtaining Author entities from a data store.
    """
    @abstractmethod
    async def obtain_by_name(self, name: str) -> Author | None: ...
