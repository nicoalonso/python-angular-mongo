from src.domain.sale import Sale
from tests.fixtures.mothers.base import BaseMother
from .customer_mother import CustomerMother
from .sale_invoice_mother import SaleInvoiceMother


class SaleMother(BaseMother):
    """Mother class for creating Sale instances for testing purposes."""

    _JOHN_DOE_SALE_1 = {
        'customer': CustomerMother.john_doe,
        'number': 'F-00001',
        'invoice': SaleInvoiceMother.john_doe_sale1,
        'created_by': 'test',
    }

    _JOHN_DOE_SALE_2 = {
        'customer': CustomerMother.john_doe,
        'number': 'F-00001',
        'invoice': SaleInvoiceMother.john_doe_sale2,
        'created_by': 'test',
    }

    @classmethod
    def john_doe_sale1(cls, **overrides) -> Sale:
        """Returns a Sale instance with the data of JOHN_DOE_SALE_1."""
        return cls._create(cls._JOHN_DOE_SALE_1, overrides)

    @classmethod
    def john_doe_sale2(cls, **overrides) -> Sale:
        """Returns a Sale instance with the data of JOHN_DOE_SALE_2."""
        return cls._create(cls._JOHN_DOE_SALE_2, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> Sale:
        """Creates a Sale instance with the given values and overrides."""
        data = cls._merge(values, overrides)
        return Sale.create(**data)
