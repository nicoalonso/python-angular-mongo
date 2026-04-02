from datetime import datetime

import pytest

from src.domain.borrow import Borrow
from src.domain.borrow.exception import InvalidBorrowNumberError
from tests.fixtures.mothers import CustomerMother


class TestBorrow:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.customer = CustomerMother.john_doe()

    def test_fail_when_invalid_number(self):
        with pytest.raises(InvalidBorrowNumberError):
            Borrow.create(customer=self.customer, number='', total_books=1, created_by='admin')

    def test_should_create_borrow(self):
        borrow = Borrow.create(customer=self.customer, number='BORROW-001', total_books=3, created_by='admin')

        assert borrow.customer == self.customer.get_descriptor()
        assert borrow.number == 'BORROW-001'
        assert borrow.total_books == 3
        assert isinstance(borrow.borrow_date, datetime)
        assert isinstance(borrow.due_date, datetime)
        assert borrow.returned is False
        assert borrow.total_returned_books == 0
        assert borrow.returned_date is None
        assert borrow.penalty is False
        assert borrow.penalty_amount == 0.0

    def test_should_run_when_modify_pending(self):
        borrow = Borrow.create(customer=self.customer, number='BORROW-001', total_books=3, created_by='admin')
        borrow.modify(returned_books=2, updated_by='admin')

        assert borrow.total_returned_books == 2
        assert borrow.returned is False
        assert borrow.returned_date is None

    def test_should_run_when_modify_returned(self):
        borrow = Borrow.create(customer=self.customer, number='BORROW-001', total_books=3, created_by='admin')
        borrow.modify(returned_books=3, updated_by='admin')

        assert borrow.total_returned_books == 3
        assert borrow.returned is True
        assert isinstance(borrow.returned_date, datetime)

    def test_should_run_when_penalize(self):
        borrow = Borrow.create(customer=self.customer, number='BORROW-001', total_books=3, created_by='admin')
        borrow.penalize(amount=10.0)

        assert borrow.penalty is True
        assert borrow.penalty_amount == 10.0
