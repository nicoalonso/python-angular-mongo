from src.domain.customer import ContactInfo
from tests.fixtures.mothers.base import BaseMother


class ContactInfoMother(BaseMother):
    """Mother class for creating ContactInfo instances for testing purposes."""

    _DOE_CONTACT_INFO = {
        'email': 'johndoe@gmail.com',
        'phone1': '+1234567890',
        'phone2': '+0987654321',
    }

    _SMITH_CONTACT_INFO = {
        'email': 'jsmith@gmail.com',
        'phone1': '+1111111111',
        'phone2': '+2222222222',
    }

    @classmethod
    def doe(cls, **overrides) -> ContactInfo:
        """Returns a ContactInfo instance with the data of DOE_CONTACT_INFO."""
        return cls._create(cls._DOE_CONTACT_INFO, overrides)

    @classmethod
    def smith(cls, **overrides) -> ContactInfo:
        """Returns a ContactInfo instance with the data of SMITH_CONTACT_INFO."""
        return cls._create(cls._SMITH_CONTACT_INFO, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> ContactInfo:
        """Creates a ContactInfo instance with the given overrides."""
        data = cls._merge(values, overrides)
        return ContactInfo(**data)
