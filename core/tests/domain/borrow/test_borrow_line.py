import pytest

from src.domain.borrow import BorrowLine
from tests.fixtures.mothers import BorrowMother, BookMother


class TestBorrowLine:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.borrow = BorrowMother.john_doe()
        self.book = BookMother.romeo_and_juliet()

    def test_should_run_when_create(self):
        borrow_line = BorrowLine.create(borrow=self.borrow, book=self.book)

        assert borrow_line.borrow == self.borrow.id
        assert borrow_line.book == self.book.get_descriptor()
        assert borrow_line.returned is False
        assert borrow_line.returned_date is None
        assert borrow_line.penalty is False
        assert borrow_line.penalty_amount == 0.0

    def test_should_run_when_check_in(self):
        borrow_line = BorrowLine.create(borrow=self.borrow, book=self.book)
        borrow_line.check_in()

        assert borrow_line.returned is True
        assert borrow_line.returned_date is not None

    def test_should_run_when_penalice(self):
        borrow_line = BorrowLine.create(borrow=self.borrow, book=self.book)
        borrow_line.penalize(amount=5.0)

        assert borrow_line.penalty is True
        assert borrow_line.penalty_amount == 5.0
