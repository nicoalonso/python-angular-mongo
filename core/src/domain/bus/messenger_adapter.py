from abc import ABC, abstractmethod
from typing import Callable


class MessengerAdapter(ABC):
    """
    MessengerAdapter interface
    """
    @abstractmethod
    def consume(self, callback: Callable) -> None: ...

    @abstractmethod
    def send(self, message: bytes, route: str) -> None: ...
