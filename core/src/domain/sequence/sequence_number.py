from dataclasses import dataclass

from src.domain.identity import Identity
from .sequence_type import SequenceType


@dataclass
class SequenceNumber(Identity):
    """
    It is used to generate unique identifiers for entities in the system.
    """
    type: SequenceType = None
    prefix: str = None
    number: int = None

    @classmethod
    def create(cls, type_: SequenceType) -> "SequenceNumber":
        return cls(
            type=type_,
            prefix=type_.get_prefix(),
            number=1,
        )

    def format(self) -> str:
        return f"{self.prefix}{self.number:05d}"

    def next(self) -> "SequenceNumber":
        self.number += 1
        return self
