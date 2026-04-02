from abc import ABC, abstractmethod
from typing import Optional

from .domain_event import DomainEvent


class MessengerSerializer(ABC):
    """
    Interface for all messenger serializers
    """
    @abstractmethod
    def encode(self, message: DomainEvent) -> Optional[dict]: ...

    @abstractmethod
    def decode(self, message: dict) -> Optional[DomainEvent]: ...
