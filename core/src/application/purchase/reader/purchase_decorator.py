from dataclasses import dataclass, asdict

from src.domain.purchase import Purchase, PurchaseLineCollection


@dataclass(slots=True)
class PurchaseDecorator:
    """Decorator class for Purchase entity that adds additional functionality without modifying the original Purchase class."""
    _purchase: Purchase
    _lines: PurchaseLineCollection

    def __getattr__(self, name: str):
        return getattr(self._purchase, name)

    def get_lines(self) -> PurchaseLineCollection:
        return self._lines

    def to_dict(self) -> dict:
        """Convert the decorated purchase to a dictionary representation."""
        return {
            **asdict(self._purchase),
            'lines': [asdict(line) for line in self._lines]
        }
