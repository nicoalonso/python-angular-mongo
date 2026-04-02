from abc import ABC, abstractmethod

from src.domain.identity import ListRepository
from .customer import Customer


class CustomerRepository(ListRepository[Customer], ABC):
    """
    Abstract base class for Customer repository.
    Defines the interface for obtaining Customer entities from a data store.
    """
    @abstractmethod
    async def obtain_by_name(self, name: str, surname: str) -> Customer | None: ...

    @abstractmethod
    async def obtain_by_number(self, number: str) -> Customer | None: ...
