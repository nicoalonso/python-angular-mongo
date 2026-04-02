from dataclasses import dataclass
from datetime import datetime


@dataclass
class Membership:
    number: str = None
    active: bool = None
    ended_at: datetime | None = None

    @classmethod
    def create(cls, number: str) -> "Membership":
        """
        Factory method to create a new Membership instance.
        """
        return cls(
            number=number,
            active=True,
            ended_at=None
        )

    def enable(self) -> None:
        """
        Enables the membership.
        """
        self.active = True
        self.ended_at = None

    def disable(self) -> None:
        """
        Disables the membership.
        """
        self.active = False
        self.ended_at = datetime.now()
