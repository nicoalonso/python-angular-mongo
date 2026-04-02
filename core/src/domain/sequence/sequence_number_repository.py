from abc import ABC, abstractmethod

from src.domain.sequence import SequenceType, SequenceNumber


class SequenceNumberRepository(ABC):
    """
    Interface for the repository that manages sequence numbers.
    """
    @abstractmethod
    async def obtain_by_type(self, type_: SequenceType) -> SequenceNumber: ...

    @abstractmethod
    async def next_number(self, type_: SequenceType) -> SequenceNumber: ...
