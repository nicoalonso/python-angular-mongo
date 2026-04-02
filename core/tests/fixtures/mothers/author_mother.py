from src.domain.author import Author
from tests.fixtures.mothers.base import MotherMapping, BaseMother


class AuthorMother(BaseMother):
    """Mother class for creating Author instances for testing purposes."""

    _SHAKESPEARE = {
        'name': 'William Shakespeare',
        'real_name': 'William Shakespeare',
        'genres': 'Tragedy, Comedy, History',
        'biography': 'William Shakespeare was an English playwright, poet, and actor.',
        'nationality': 'English',
        'birth_date': ['1564-04-23', MotherMapping.DATE],
        'death_date': ['1616-04-23', MotherMapping.DATE],
        'photo_url': 'https://example.com/shakespeare.jpg',
        'website': 'https://en.wikipedia.org/wiki/William_Shakespeare',
        'created_by': 'test',
    }

    _CERVANTES = {
        'name': 'Miguel de Cervantes',
        'real_name': 'Miguel de Cervantes Saavedra',
        'genres': 'Novel, Drama, Poetry',
        'biography':
            'Miguel de Cervantes was a Spanish writer widely regarded as one of the greatest writers in the Spanish language.',
        'nationality': 'Spanish',
        'birth_date': ['1547-09-29', MotherMapping.DATE],
        'death_date': ['1616-04-22', MotherMapping.DATE],
        'photo_url': 'https://example.com/cervantes.jpg',
        'website': 'https://en.wikipedia.org/wiki/Miguel_de_Cervantes',
        'created_by': 'test',
    }

    @classmethod
    def shakespeare(cls, **overrides) -> Author:
        """Returns an author representing William Shakespeare."""
        return cls._create(cls._SHAKESPEARE, overrides)

    @classmethod
    def cervantes(cls, **overrides) -> Author:
        """Returns an author representing William Shakespeare."""
        return cls._create(cls._CERVANTES, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> Author:
        """Creates an Author instance with the given values and overrides."""
        data = cls._merge(values, overrides)
        return Author(**data)
