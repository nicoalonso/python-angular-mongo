from abc import ABC, abstractmethod

from .user import User


class UserRepository(ABC):
    @abstractmethod
    def obtain_user(self) -> User: ...

    @abstractmethod
    def remove_user(self, user: User) -> None: ...

    @abstractmethod
    def save(self, user: User) -> None: ...
