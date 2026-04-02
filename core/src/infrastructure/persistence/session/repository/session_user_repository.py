from src.domain.user import User
from src.domain.user.user_repository import UserRepository


class SessionUserRepository(UserRepository):
    """
    Repository for managing user sessions. This repository is responsible for storing and retrieving user information during a session.
    To emulate for exemplary purposes
    """
    def obtain_user(self) -> User:
        return User('jdoe@gmail.com', 'John Doe', ['admin'])

    def remove_user(self, user: User) -> None:
        pass

    def save(self, user: User) -> None:
        pass
