import pytest

from src.domain.services.book_inspector import *
from tests.doubles.infrastructure.persistence import BorrowLineRepositoryStub


class TestBookInspectFactory:
    @pytest.fixture(autouse=True)
    def setup(self):
        repo_borrow_line = BorrowLineRepositoryStub()
        self.factory = BookInspectFactory(repo_borrow_line)

    def test_create_borrow_inspector(self):
        inspector = self.factory.create(is_sale=False)

        assert isinstance(inspector, BookBorrowInspect)

    def test_create_sale_inspector(self):
        inspector = self.factory.create(is_sale=True)

        assert isinstance(inspector, BookSaleInspect)
