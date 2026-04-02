from src.domain.purchase import Purchase
from tests.fixtures.mothers.base import BaseMother, MotherMapping
from .provider_mother import ProviderMother
from .purchase_invoice_mother import PurchaseInvoiceMother


class PurchaseMother(BaseMother):
    """Mother class for creating Purchase instances for testing purposes."""

    _AMAZON_INV_1 = {
        'provider': ProviderMother.amazon,
        'purchased_at': ['2026-03-02', MotherMapping.DATE],
        'invoice': PurchaseInvoiceMother.invoice1,
        'created_by': 'test',
    }

    _BEST_BUY_INV_2 = {
        'provider': ProviderMother.best_buy,
        'purchased_at': ['2026-03-02', MotherMapping.DATE],
        'invoice': PurchaseInvoiceMother.invoice2,
        'created_by': 'test',
    }

    @classmethod
    def amazon_inv1(cls, **overrides) -> Purchase:
        """Returns a Purchase instance with the data of AMAZON_INV_1."""
        return cls._create(cls._AMAZON_INV_1, overrides)

    @classmethod
    def best_buy_inv2(cls, **overrides) -> Purchase:
        """Returns a Purchase instance with the data of BEST_BUY_INV_2."""
        return cls._create(cls._BEST_BUY_INV_2, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> Purchase:
        """Creates a Purchase instance with the given values and overrides."""
        data = cls._merge(values, overrides)
        return Purchase.create(**data)
