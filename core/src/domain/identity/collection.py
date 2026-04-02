from collections.abc import Callable
from typing import overload, Optional

from typing_extensions import TypeVar, Generic

T = TypeVar('T')
U = TypeVar('U')


class Collection(Generic[T]):
    """
    Collection of items

    Attributes:
        items: (list[T]) List of items
    """
    def __init__(self, items: Optional[list[T]] = None):
        self.items: list[T] = items or []

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> list[T]: ...

    def __getitem__(self, index: int | slice) -> T | list[T]:
        # noinspection PyTypeChecker
        return self.items[index]

    def __contains__(self, item: object) -> bool:
        return item in self.items

    def __bool__(self) -> bool:
        return len(self.items) > 0

    def to_array(self) -> list[T]:
        """
        Convert the collection to array

        :return: array of items
        """
        return self.items

    def count(self) -> int:
        """
        Count the number of items in the collection

        :return: number of items
        """
        return len(self.items)

    def is_empty(self) -> bool:
        """
        Check if the collection is empty

        :return: True if the collection is empty, False otherwise
        """
        return len(self.items) == 0

    def first(self) -> T | None:
        """
        Get the first item of the collection

        :return: first item of the collection, None if the collection is empty
        """
        return self.items[0] if self.items else None

    def last(self) -> T | None:
        """
        Get the last item of the collection

        :return: last item of the collection, None if the collection is empty
        """
        return self.items[-1] if self.items else None

    def add(self, item: T) -> None:
        """
        Add an item to the collection

        :param item: item to be added
        """
        self.items.append(item)

    def get(self, index: int) -> T | None:
        """
        Get an item by index

        :param index: index of the item to be retrieved
        :return: item at the specified index
        """
        if index < 0 or index >= len(self.items):
            return None

        return self.items[index]

    def set(self, index: int, item: T) -> None:
        """
        Set an item by index

        :param index: index of the item to be set
        :param item: item to be set
        """
        if index < 0 or index >= len(self.items):
            return

        self.items[index] = item

    def remove(self, item: T) -> bool:
        """
        Remove an item from the collection

        :param item: item to be removed
        """
        if item in self.items:
            self.items.remove(item)
            return True

        return False

    def clear(self) -> None:
        """
        Clear the collection
        """
        self.items.clear()

    def map(self, func: Callable[[T], U]) -> 'Collection[U]':
        """
        Map a function to the items of the collection

        :param func: function to be applied to the items
        :return: new collection with the mapped items
        """
        return Collection([func(item) for item in self.items])

    def filter(self, func: Callable[[T], bool]) -> 'Collection[T]':
        """
        Filter the items of the collection by a function

        :param func: function to be applied to the items
        :return: new collection with the filtered items
        """
        return Collection([item for item in self.items if func(item)])

    def find_first(self, func: Callable[[T], bool]) -> T | None:
        """
        Find the first item that matches a condition

        :param func: function to be applied to the items
        :return: first item that matches the condition, None if no item matches
        """
        for item in self.items:
            if func(item):
                return item

        return None

    def exists(self, func: Callable[[T], bool]) -> bool:
        """
        Check if there is an item that matches a condition

        :param func: function to be applied to the items
        :return: True if there is an item that matches the condition, False otherwise
        """
        return any(func(item) for item in self.items)

    def index_of(self, item: T) -> int:
        """
        Get the index of an item in the collection

        :param item: (T) item to get the index of
        :return: (int) index of the item, -1 if the item is not found
        """
        try:
            return self.items.index(item)
        except ValueError:
            return -1
