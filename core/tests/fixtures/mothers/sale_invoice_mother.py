from src.domain.sale import SaleInvoice
from tests.fixtures.mothers.base import BaseMother, MotherMapping


class SaleInvoiceMother(BaseMother):
    """Mother class for creating SaleInvoice instances for testing purposes."""
    _JOHN_DOE_SALE_1 = {
        'date': ['2024-01-01', MotherMapping.DATE],
        'amount': 100,
        'tax_percentage': 21,
        'taxes': 21,
        'total': 121,
    }

    _JOHN_DOE_SALE_2 = {
        'date': ['2026-03-06', MotherMapping.DATE],
        'amount': 80,
        'tax_percentage': 21,
        'taxes': 16.8,
        'total': 96.8,
    }

    @classmethod
    def john_doe_sale1(cls, **overrides) -> SaleInvoice:
        """Returns a SaleInvoice instance with the data of JOHN_DOE_SALE_1."""
        return cls._create(cls._JOHN_DOE_SALE_1, overrides)

    @classmethod
    def john_doe_sale2(cls, **overrides) -> SaleInvoice:
        """Returns a SaleInvoice instance with the data of JOHN_DOE_SALE_2."""
        return cls._create(cls._JOHN_DOE_SALE_2, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> SaleInvoice:
        """Creates a SaleInvoice instance with the given overrides."""
        data = cls._merge(values, overrides)
        return SaleInvoice(**data)
