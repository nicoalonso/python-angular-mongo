from src.domain.borrow.borrow import Borrow
from tests.fixtures.mothers.base import BaseMother
from .customer_mother import CustomerMother


class BorrowMother(BaseMother):
    """Mother class for Borrow entity."""

    _JOHN_DOE = {
        'customer': CustomerMother.john_doe,
        'number': 'P-00022',
        'total_books': 3,
        'created_by': 'test',
    }

    @classmethod
    def john_doe(cls, **overrides) -> Borrow:
        """Returns a Borrow instance for John Doe with optional overrides."""
        return cls._create(cls._JOHN_DOE, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> Borrow:
        """Creates a Borrow instance with the given values and overrides."""
        data = cls._merge(values, overrides)
        return Borrow.create(**data)
