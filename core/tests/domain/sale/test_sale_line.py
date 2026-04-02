import pytest

from src.domain.sale import SaleLine
from tests.fixtures.mothers import BookMother, SaleMother


class TestSaleLine:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.sale = SaleMother.john_doe_sale1()
        self.book = BookMother.don_quijote()

    def test_should_create(self):
        sale_line = SaleLine.create(
            sale=self.sale,
            book=self.book,
            quantity=2,
            price=10.0,
            discount=0.0,
            total=20.0,
        )

        assert sale_line.sale == self.sale.id
        assert sale_line.book == self.book.get_descriptor()
        assert sale_line.quantity == 2
        assert sale_line.price == 10.0
        assert sale_line.discount == 0.0
        assert sale_line.total == 20.0

    def test_should_run_when_modify(self):
        sale_line = SaleLine.create(
            sale=self.sale,
            book=self.book,
            quantity=2,
            price=10.0,
            discount=0.0,
            total=20.0,
        )

        sale_line.modify(
            book=self.book,
            quantity=3,
            price=9.0,
            discount=1.0,
            total=26.0,
        )

        assert sale_line.quantity == 3
        assert sale_line.price == 9.0
        assert sale_line.discount == 1.0
        assert sale_line.total == 26.0
