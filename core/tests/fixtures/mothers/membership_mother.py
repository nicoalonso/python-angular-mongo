from src.domain.customer import Membership
from tests.fixtures.mothers.base import BaseMother


class MembershipMother(BaseMother):
    """Mother class for creating Membership entities for testing purposes."""
    _ACTIVE = {
        'number': 'SN00025',
    }

    @classmethod
    def active(cls, **overrides) -> Membership:
        """Returns an active Membership instance."""
        return cls._create(cls._ACTIVE, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> Membership:
        data = cls._merge(values, overrides)
        return Membership.create(**data)
