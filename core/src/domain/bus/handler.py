from abc import ABC, abstractmethod

from src.domain.bus import DomainEvent


class Handler(ABC):
    """
    Base class for all handlers in the system.
    """
    @abstractmethod
    async def handle(self, event: DomainEvent): ...
