from enum import Enum

from src.domain.identity import Collection
from src.domain.identity.list import FieldBase


class SortDirection(Enum):
    Ascending = 'asc'
    Descending = 'desc'


class SortField(FieldBase):
    """
    A sort field represents a field that can be used for sorting in a list.

    :ivar direction: (SortDirection) The direction of the sort, either ascending or descending.
    """
    def __init__(
            self,
            name: str,
            *,
            direction: SortDirection = SortDirection.Ascending,
    ):
        super().__init__(name)
        self.direction: SortDirection = direction

    @staticmethod
    def from_string(sort_value: str) -> 'SortField':
        """
        Creates a SortField instance from a string representation of the sort field.

        The string should be in the format "[+,-]field_name",
        where `+` is ascending direction and `-` is descending direction".

        :param sort_value: The string representation of the sort field.
        :return: A SortField instance based on the provided string.
        """
        name = sort_value
        direction = SortDirection.Ascending

        if sort_value.startswith('+'):
            name = sort_value[1:]
            direction = SortDirection.Ascending
        elif sort_value.startswith('-'):
            name = sort_value[1:]
            direction = SortDirection.Descending

        return SortField(name, direction=direction)

    def is_ascending(self) -> bool:
        """
        Checks if the sort direction is ascending.

        :return: True if the sort direction is ascending, False otherwise.
        """
        return self.direction == SortDirection.Ascending

    def is_descending(self) -> bool:
        """
        Checks if the sort direction is descending.

        :return: True if the sort direction is descending, False otherwise.
        """
        return self.direction == SortDirection.Descending


type SortFieldCollection = Collection[SortField]
