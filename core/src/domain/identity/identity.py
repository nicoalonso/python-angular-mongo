import uuid
from dataclasses import dataclass, field


@dataclass
class Identity:
    """
    Identity is a base class that provides a unique identifier for entities.
    It can be used as a base class for any entity that requires a unique identifier.
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Identity):
            return False

        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
