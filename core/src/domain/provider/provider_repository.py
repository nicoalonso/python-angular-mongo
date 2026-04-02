from abc import ABC, abstractmethod

from src.domain.identity import ListRepository
from .provider import Provider


class ProviderRepository(ListRepository[Provider], ABC):
    """
    Abstract base class for Provider repository.
    Defines the interface for obtaining Provider entities from a data store.
    """
    @abstractmethod
    async def obtain_by_name(self, name: str) -> Provider | None: ...
