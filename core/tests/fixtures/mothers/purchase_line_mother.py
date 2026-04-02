from src.domain.purchase import PurchaseLine
from tests.fixtures.mothers.base import BaseMother
from .purchase_mother import PurchaseMother
from .book_mother import BookMother


class PurchaseLineMother(BaseMother):
    """Mother class for PurchaseLine entity."""

    _AMAZON_LINE_1 = {
        'purchase': PurchaseMother.amazon_inv1(),
        'book': BookMother.romeo_and_juliet(),
        'quantity': 2,
        'unit_price': 10.0,
        'discount_percentage': 5.0,
        'total': 19.0,
    }

    _AMAZON_LINE_2 = {
        'purchase': PurchaseMother.amazon_inv1(),
        'book': BookMother.don_quijote(),
        'quantity': 3,
        'unit_price': 15.0,
        'discount_percentage': 10.0,
        'total': 40.5,
    }

    _BEST_BUY_LINE_1 = {
        'purchase': PurchaseMother.best_buy_inv2(),
        'book': BookMother.romeo_and_juliet(),
        'quantity': 1,
        'unit_price': 20.0,
        'discount_percentage': 0.0,
        'total': 20.0,
    }

    @classmethod
    def amazon_line1(cls, **overrides) -> PurchaseLine:
        """Returns a PurchaseLine instance for Amazon Line 1 with optional overrides."""
        return cls._create(cls._AMAZON_LINE_1, overrides)

    @classmethod
    def amazon_line2(cls, **overrides) -> PurchaseLine:
        """Returns a PurchaseLine instance for Amazon Line 2 with optional overrides."""
        return cls._create(cls._AMAZON_LINE_2, overrides)

    @classmethod
    def best_buy_line1(cls, **overrides) -> PurchaseLine:
        """Returns a PurchaseLine instance for Best Buy Line 1 with optional overrides."""
        return cls._create(cls._BEST_BUY_LINE_1, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> PurchaseLine:
        """Creates a PurchaseLine instance with given values and overrides."""
        data = cls._merge(values, overrides)
        return PurchaseLine.create(**data)
