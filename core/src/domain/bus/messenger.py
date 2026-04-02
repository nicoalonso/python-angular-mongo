from abc import ABC, abstractmethod

from .domain_event import DomainEvent
from .messenger_adapter import MessengerAdapter
from .messenger_serializer import MessengerSerializer


class Messenger(ABC):
    """
    Messenger Interfaz

    :ivar adapter: MessengerAdapter - messenger adapter
    :ivar serializers: dict[str, MessengerSerializer] - dict of serializers
    """
    def __init__(self, adapter: MessengerAdapter):
        self.adapter = adapter
        self.serializers: dict[str, MessengerSerializer] = {}

    def add_serializer(self, action: str, serializer: MessengerSerializer) -> None:
        """
        Add serializer to messenger
        :param action: str - action name
        :param serializer: MessengerSerializer - serializer
        """
        self.serializers[action] = serializer

    @abstractmethod
    async def consume(self) -> None: ...

    @abstractmethod
    def send(self, message: DomainEvent) -> None: ...
