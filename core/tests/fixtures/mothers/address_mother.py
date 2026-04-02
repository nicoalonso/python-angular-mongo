from src.domain.common import Address
from tests.fixtures.mothers.base import BaseMother


class AddressMother(BaseMother):
    """Mother class for creating Address instances for testing purposes."""

    _ANYTOWN = {
        'street': '123 Main Street',
        'postal_code': '12345',
        'city': 'Anytown',
        'province': 'Alaska',
        'country': 'EEUU',
    }

    _NEWTON = {
        'street': '456 Elm Street',
        'postal_code': '67890',
        'city': 'Newton',
        'province': 'Massachusetts',
        'country': 'EEUU',
    }

    @classmethod
    def anytown(cls, **overrides) -> Address:
        """Returns an Address instance representing Anytown."""
        return cls._create(cls._ANYTOWN, overrides)

    @classmethod
    def newtown(cls, **overrides) -> Address:
        """Returns an Address instance representing Newton."""
        return cls._create(cls._NEWTON, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> Address:
        """Creates an Address instance with the given overrides."""
        data = cls._merge(values, overrides)
        return Address(**data)
