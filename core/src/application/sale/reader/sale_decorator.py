from dataclasses import dataclass, asdict

from src.domain.sale import Sale, SaleLineCollection


@dataclass(slots=True)
class SaleDecorator:
    """Decorator class for Sale entity that adds additional functionality without modifying the original Sale class."""
    _sale: Sale
    _lines: SaleLineCollection

    def __getattr__(self, name: str):
        return getattr(self._sale, name)

    def get_lines(self) -> SaleLineCollection:
        return self._lines

    def to_dict(self) -> dict:
        """Convert the decorated sale to a dictionary representation."""
        return {
            **asdict(self._sale),
            'lines': [asdict(line) for line in self._lines]
        }
