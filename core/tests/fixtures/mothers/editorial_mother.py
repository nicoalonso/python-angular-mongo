from src.domain.editorial import Editorial
from tests.fixtures.mothers import EnterpriseContactMother, AddressMother
from tests.fixtures.mothers.base import BaseMother


class EditorialMother(BaseMother):
    """Mother class for creating Editorial instances for testing purposes."""

    _ANAYA = {
        'name': 'Anaya',
        'comercial_name': 'Anaya Inc.',
        'contact': EnterpriseContactMother.anaya,
        'address': AddressMother.anytown,
        'created_by': 'test',
    }

    @classmethod
    def anaya(cls, **overrides) -> Editorial:
        """Returns an editorial representing Anaya."""
        return cls._create(cls._ANAYA, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> Editorial:
        """Creates an Editorial instance with the given values and overrides."""
        data = cls._merge(values, overrides)
        return Editorial(**data)
