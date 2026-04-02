from abc import ABC, abstractmethod
from typing import Optional

from .domain_event import DomainEvent
from .handler import Handler
from .messenger import Messenger


class DomainBus(ABC):
    """
    Interface for a domain bus

    :ivar initialize: bool - indicates if the bus is initialized
    :ivar messenger: Optional[Messenger] - messenger for the transport layer
    """
    def __init__(self):
        self.initialize = True
        self.messenger: Optional[Messenger] = None

    @abstractmethod
    async def dispatch(self, event: DomainEvent): ...

    @abstractmethod
    def register_handler(self, event_type: type[DomainEvent], handler: Handler) -> None: ...

    def registered(self):
        """ Marks the bus as initialized and ready to dispatch events """
        self.initialize = False

    def set_messenger(self, messenger: Messenger) -> None:
        """
        Sets the messenger for the bus

        :param messenger: Messenger
        :return:
        """
        self.messenger = messenger

    def send(self, event: DomainEvent) -> None:
        """
        Sends an event through the messenger

        :param event: DomainEvent
        """
        if self.messenger is not None:
            self.messenger.send(event)
