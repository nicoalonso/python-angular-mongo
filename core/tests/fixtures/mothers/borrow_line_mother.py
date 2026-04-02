from src.domain.borrow.borrow_line import BorrowLine
from tests.fixtures.mothers.base import BaseMother
from .borrow_mother import BorrowMother
from .book_mother import BookMother


class BorrowLineMother(BaseMother):
    """Mother class for BorrowLine entity."""

    _ROMEO_AND_JULIET = {
        'borrow': BorrowMother.john_doe,
        'book': BookMother.romeo_and_juliet,
    }

    _DON_QUIJOTE = {
        'borrow': BorrowMother.john_doe,
        'book': BookMother.don_quijote,
    }

    @classmethod
    def romeo_and_juliet(cls, **overrides) -> BorrowLine:
        """Returns a BorrowLine instance for Romeo and Juliet with optional overrides."""
        return cls._create(cls._ROMEO_AND_JULIET, overrides)

    @classmethod
    def don_quijote(cls, **overrides) -> BorrowLine:
        """Returns a BorrowLine instance for Don Quixote with optional overrides."""
        return cls._create(cls._DON_QUIJOTE, overrides)

    @classmethod
    def _create(cls, values: dict, overrides: dict) -> BorrowLine:
        """Creates a BorrowLine instance with given values and overrides."""
        data = cls._merge(values, overrides)
        return BorrowLine.create(**data)
