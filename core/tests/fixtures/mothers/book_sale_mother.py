from src.domain.book import BookSale
from tests.fixtures.mothers.base import BaseMother


class BookSaleMother(BaseMother):
    """Mother class for creating BookSale instances for testing purposes."""

    _VALID = {
        'saleable': True,
        'price': 100.0,
        'discount': 10.0,
    }

    @classmethod
    def valid(cls, **overrides) -> BookSale:
        """Returns a valid BookSale instance."""
        return cls._create(cls._VALID, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> BookSale:
        """Creates a BookSale instance with the given overrides."""
        data = cls._merge(values, overrides)
        return BookSale(**data)
