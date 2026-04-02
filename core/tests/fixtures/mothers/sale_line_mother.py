from src.domain.sale import SaleLine
from tests.fixtures.mothers.base import BaseMother
from .sale_mother import SaleMother
from .book_mother import BookMother


class SaleLineMother(BaseMother):
    """Mother class for SaleLine entity."""

    _JOHN_SALE_1_LINE_1 = {
        'sale': SaleMother.john_doe_sale1,
        'book': BookMother.don_quijote,
        'quantity': 2,
        'price': 10.0,
        'discount': 0.0,
        'total': 20.0,
    }

    _JOHN_SALE_1_LINE_2 = {
        'sale': SaleMother.john_doe_sale1,
        'book': BookMother.romeo_and_juliet,
        'quantity': 1,
        'price': 12.0,
        'discount': 0.0,
        'total': 12.0,
    }

    _JOHN_SALE_2_LINE_1 = {
        'sale': SaleMother.john_doe_sale2,
        'book': BookMother.romeo_and_juliet,
        'quantity': 3,
        'price': 11.0,
        'discount': 5.0,
        'total': 31.35,
    }

    @classmethod
    def john_sale1_line1(cls, **overrides) -> SaleLine:
        """Returns a SaleLine instance for John Doe's Sale 1 Line 1 with optional overrides."""
        return cls._create(cls._JOHN_SALE_1_LINE_1, overrides)

    @classmethod
    def john_sale1_line2(cls, **overrides) -> SaleLine:
        """Returns a SaleLine instance for John Doe's Sale 1 Line 2 with optional overrides."""
        return cls._create(cls._JOHN_SALE_1_LINE_2, overrides)

    @classmethod
    def john_sale2_line1(cls, **overrides) -> SaleLine:
        """Returns a SaleLine instance for John Doe's Sale 2 Line 1 with optional overrides."""
        return cls._create(cls._JOHN_SALE_2_LINE_1, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> SaleLine:
        """Creates a SaleLine instance with given values and overrides."""
        data = cls._merge(values, overrides)
        return SaleLine.create(**data)
