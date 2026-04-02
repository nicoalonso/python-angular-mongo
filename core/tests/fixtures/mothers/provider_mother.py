from src.domain.provider import Provider
from tests.fixtures.mothers import EnterpriseContactMother, AddressMother
from tests.fixtures.mothers.base import BaseMother


class ProviderMother(BaseMother):
    """Mother class for creating Provider instances for testing purposes."""

    _AMAZON = {
        'name': 'Amazon',
        'comercial_name': 'Amazon, Inc.',
        'contact': EnterpriseContactMother.amazon,
        'address': AddressMother.anytown,
        'vat_number': 'B36565656',
        'created_by': 'test',
    }

    _BEST_BUY = {
        'name': 'Best Buy',
        'comercial_name': 'Best Buy Co., Inc.',
        'contact': EnterpriseContactMother.best_buy,
        'address': AddressMother.anytown,
        'vat_number': 'B36565656',
        'created_by': 'test',
    }

    @classmethod
    def amazon(cls, **overrides) -> Provider:
        """Returns a generic provider instance."""
        return cls._create(cls._AMAZON, overrides)

    @classmethod
    def best_buy(cls, **overrides) -> Provider:
        """Returns a generic provider instance."""
        return cls._create(cls._BEST_BUY, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> Provider:
        """Creates a Provider instance with the given values and overrides."""
        data = cls._merge(values, overrides)
        return Provider(**data)
