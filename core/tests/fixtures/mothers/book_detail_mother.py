from src.domain.book import BookDetail
from tests.fixtures.mothers.base import BaseMother, MotherMapping


class BookDetailMother(BaseMother):
    """Mother class for creating BookDetail instances for testing purposes."""
    _VALID = {
        'edition': '001',
        'isbn': '978-1234567890',
        'language': 'English',
        'published_at': ['2020-01-01', MotherMapping.DATE],
        'pages': 100,
    }

    _QUIJOTE = {
        'edition': '001',
        'isbn': '978-1234567890',
        'language': 'Spanish',
        'published_at': ['1615-01-01', MotherMapping.DATE],
        'pages': 100,
    }

    @classmethod
    def valid(cls, **overrides) -> BookDetail:
        """Returns a valid BookDetail instance."""
        return cls._create(cls._VALID, overrides)

    @classmethod
    def quijote(cls, **overrides) -> BookDetail:
        """Returns a BookDetail instance representing Don Quijote."""
        return cls._create(cls._QUIJOTE, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> BookDetail:
        """Creates a BookDetail instance with the given overrides."""
        data = cls._merge(values, overrides)
        return BookDetail(**data)
