from typing import Optional, cast

from src.domain.user import User
from src.domain.user.user_repository import UserRepository


class UserRepositoryStub(UserRepository):
    """
    User repository stub for testing purposes.
    """
    def __init__(self):
        self.user: Optional[User] = None
        self.stored: Optional[User] = None
        self.removed: bool = False
        self._exception: Optional[Exception] = None

        self.change_user()

    def obtain_user(self) -> User:
        self._throw_error()
        return cast(User, self.user)

    def remove_user(self, user: User) -> None:
        self._throw_error()
        self.removed = True

    def save(self, user: User) -> None:
        self.stored = user

    def normal_user(self) -> None:
        self.change_user(groups=['user'])

    def change_user(
            self,
            name: str = 'jdoe@gmail.com',
            display_name: str = 'John Doe',
            groups: Optional[list[str]] = None
    ) -> None:
        self.user = User(
            name,
            display_name,
            groups if groups is not None else ['admin']
        )

    def error(self, exception: Exception | str) -> None:
        if isinstance(exception, str):
            exception = Exception(exception)
        self._exception = cast(Exception, exception)

    def _throw_error(self):
        if self._exception:
            raise self._exception
