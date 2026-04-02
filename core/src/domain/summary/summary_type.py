from __future__ import annotations

from enum import Enum


class SummaryType(str, Enum):
    """
    Enum for summary types.
    """
    DESCRIPTION = 'description'
    BIOGRAPHY = 'biography'

    @classmethod
    def try_from(cls, value: str) -> SummaryType:
        """
        Create an EnumSummaryType instance from a string value.

        :param value: (str) The string representation of the summary type.
        """
        try:
            return cls(value)
        except ValueError:
            return cls.DESCRIPTION
