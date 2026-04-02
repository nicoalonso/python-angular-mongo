from abc import ABC, abstractmethod

from src.domain.identity import ListRepository
from .editorial import Editorial


class EditorialRepository(ListRepository[Editorial], ABC):
    """
    Abstract base class for Editorial repository.
    Defines the interface for obtaining Editorial entities from a data store.
    """
    @abstractmethod
    async def obtain_by_name(self, name: str) -> Editorial | None: ...
