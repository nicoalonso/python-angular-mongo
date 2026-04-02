from tests.fixtures.mothers.base import BaseMother

from src.domain.purchase import PurchaseInvoice


class PurchaseInvoiceMother(BaseMother):
    """Mother class for creating PurchaseInvoice instances for testing purposes."""

    _INVOICE_1 = {
        'number': 'INV-001',
        'amount': 100.0,
        'taxes': 20.0,
        'total': 120.0,
    }

    _INVOICE_2 = {
        'number': 'INV-002',
        'amount': 135.0,
        'taxes': 45.0,
        'total': 180.0,
    }

    @classmethod
    def invoice1(cls, **overrides) -> PurchaseInvoice:
        """Returns a PurchaseInvoice instance with the data of INVOICE_1."""
        return cls._create(cls._INVOICE_1, overrides)

    @classmethod
    def invoice2(cls, **overrides) -> PurchaseInvoice:
        """Returns a PurchaseInvoice instance with the data of INVOICE_2."""
        return cls._create(cls._INVOICE_2, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> PurchaseInvoice:
        """Creates a PurchaseInvoice instance with the given overrides."""
        data = cls._merge(values, overrides)
        return PurchaseInvoice(**data)
