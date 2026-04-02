from dataclasses import dataclass, asdict

from src.domain.borrow import Borrow, BorrowLineCollection


@dataclass(slots=True)
class BorrowDecorator:
    """Decorator class for Borrow entity that adds additional functionality without modifying the original Borrow class."""
    _borrow: Borrow
    _lines: BorrowLineCollection

    def __getattr__(self, name: str):
        return getattr(self._borrow, name)

    def get_lines(self) -> BorrowLineCollection:
        return self._lines

    def to_dict(self) -> dict:
        """Convert the decorated borrow to a dictionary representation."""
        return {
            **asdict(self._borrow),
            'lines': [asdict(line) for line in self._lines]
        }
