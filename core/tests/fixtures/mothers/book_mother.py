from src.domain.book import Book
from tests.fixtures.mothers.base import BaseMother
from .author_mother import AuthorMother
from .book_detail_mother import BookDetailMother
from .book_sale_mother import BookSaleMother
from .editorial_mother import EditorialMother


class BookMother(BaseMother):
    """
    A mother class for creating Book fixtures.
    """
    _ROMEO_AND_JULIET = {
        'title': 'Romeo and Juliet',
        'description':
            'Romeo and Juliet is a tragedy written by William Shakespeare early in his career about two young star-crossed lovers whose deaths ultimately reconcile their feuding families.',
        'author': AuthorMother.shakespeare,
        'editorial': EditorialMother.anaya,
        'detail': BookDetailMother.valid,
        'sale': BookSaleMother.valid,
        'created_by': 'test',
    }

    _DON_QUIJOTE = {
        'title': 'Don Quijote',
        'description':
            'Don Quijote de la Mancha is a Spanish novel by Miguel de Cervantes. It follows the adventures of a nobleman who reads so many chivalric romances that he loses his sanity and decides to become a knight-errant, reviving chivalry and serving his nation.',
        'author': AuthorMother.cervantes,
        'editorial': EditorialMother.anaya,
        'detail': BookDetailMother.quijote,
        'sale': BookSaleMother.valid,
        'created_by': 'test',
    }

    @classmethod
    def romeo_and_juliet(cls, **overrides) -> Book:
        """
        Creates a Book instance for "Romeo and Juliet" with optional overrides.
        """
        return cls._create(cls._ROMEO_AND_JULIET, overrides)

    @classmethod
    def don_quijote(cls, **overrides) -> Book:
        """
        Creates a Book instance for "Don Quijote" with optional overrides.
        """
        return cls._create(cls._DON_QUIJOTE, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> Book:
        """
        Creates a Book instance with the given values and overrides.
        """
        data = cls._merge(values, overrides)
        return Book.create(**data)
