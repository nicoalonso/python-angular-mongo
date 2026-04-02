from src.domain.common import EnterpriseContact
from tests.fixtures.mothers.base import BaseMother


class EnterpriseContactMother(BaseMother):
    """Mother class for creating ContactEnterprise instances for testing purposes."""

    _AMAZON = {
        'email': 'info@amazon.com',
        'website': 'https://www.amazon.com',
        'phone1': '+1-800-123-4567',
        'phone2': '+1-800-987-6543',
    }

    _BEST_BUY = {
        'email': 'info@bestbuy.com',
        'website': 'https://www.bestbuy.com',
        'phone1': '+1-800-123-4567',
        'phone2': '+1-800-987-6543',
    }

    _ANAYA = {
        'email': 'info@anaya.com',
        'website': 'https://www.anaya.com',
        'phone1': '+34-900-123-456',
        'phone2': '+34-900-987-654',
    }

    @classmethod
    def amazon(cls, **overrides) -> EnterpriseContact:
        """Returns an EnterpriseContact instance representing Amazon."""
        return cls._create(cls._AMAZON, overrides)

    @classmethod
    def best_buy(cls, **overrides) -> EnterpriseContact:
        """Returns an EnterpriseContact instance representing Best Buy."""
        return cls._create(cls._BEST_BUY, overrides)

    @classmethod
    def anaya(cls, **overrides) -> EnterpriseContact:
        """Returns an EnterpriseContact instance representing Anaya."""
        return cls._create(cls._ANAYA, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> EnterpriseContact:
        """Creates a ContactEnterprise instance with the given overrides."""
        data = cls._merge(values, overrides)
        return EnterpriseContact(**data)
