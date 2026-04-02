from src.domain.summary import Summary, SummaryType
from tests.fixtures.mothers.base import BaseMother


class SummaryMother(BaseMother):
    """Mother for Summary objects."""

    _DESCRIPTION = {
        'url': 'https://example.com/document',
        'type_': SummaryType.DESCRIPTION,
        'created_by': 'test_user',
    }

    _BIOGRAPHY = {
        'url': 'https://example.com/document',
        'type_': SummaryType.BIOGRAPHY,
        'created_by': 'test_user',
    }

    @classmethod
    def description(cls, **overrides) -> Summary:
        """Creates a Summary instance with type DESCRIPTION."""
        return cls._create(cls._DESCRIPTION, overrides)

    @classmethod
    def biography(cls, **overrides) -> Summary:
        """Creates a Summary instance with type BIOGRAPHY."""
        return cls._create(cls._BIOGRAPHY, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> Summary:
        """Creates a Summary instance with the given values and overrides."""
        data = cls._merge(values, overrides)
        return Summary.create(**data)
