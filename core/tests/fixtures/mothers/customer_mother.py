from src.domain.customer import Customer
from tests.fixtures.mothers.base import BaseMother
from .address_mother import AddressMother
from .contact_info_mother import ContactInfoMother
from .membership_mother import MembershipMother


class CustomerMother(BaseMother):
    """Mother class for Customer entity."""

    _JOHN_DOE = {
        'name': 'John',
        'surname': 'Doe',
        'membership': MembershipMother.active,
        'contact': ContactInfoMother.doe,
        'address': AddressMother.anytown,
        'vat_number': '12345667A',
        'created_by': 'test',
    }

    @classmethod
    def john_doe(cls, **overrides) -> Customer:
        """Returns a generic Customer instance."""
        return cls._create(cls._JOHN_DOE, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> Customer:
        """Creates a Customer instance with the given values and overrides."""
        data = cls._merge(values, overrides)
        return Customer.create(**data)
