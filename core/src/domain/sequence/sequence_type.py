from enum import Enum
from typing import Optional


class SequenceType(Enum):
    """
    Enum representing the type of sequence.
    """
    Membership = "membership"
    Sale = "sale"
    Borrow = "borrow"

    @classmethod
    def try_from(cls, value: str) -> Optional["SequenceType"]:
        """
        Create a SequenceType instance from a string value.

        :param value: (str) The string representation of the sequence type.
        """
        try:
            return cls(value)
        except ValueError:
            return None

    def get_prefix(self) -> str:
        """
        Get the prefix associated with the sequence type.

        :return: The prefix for the sequence type.
        """
        match self:
            case SequenceType.Membership:
                return "SN"
            case SequenceType.Sale:
                return "F-"
            case SequenceType.Borrow:
                return "P-"
