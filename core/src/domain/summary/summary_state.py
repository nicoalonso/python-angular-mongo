from __future__ import annotations

from enum import Enum


class SummaryState(str, Enum):
    """
    Enum for summary states.
    """
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'

    @classmethod
    def try_from(cls, value: str) -> SummaryState:
        """
        Create a SummaryState instance from a string value.

        :param value: (str) The string representation of the summary state.
        """
        try:
            return cls(value)
        except ValueError:
            return cls.PENDING
