import pytest

from src.domain.purchase import PurchaseLine
from tests.fixtures.mothers import BookMother, PurchaseMother


class TestPurchaseLine:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.purchase = PurchaseMother.amazon_inv1()
        self.book = BookMother.romeo_and_juliet()

    def test_should_run_create(self):
        line = PurchaseLine.create(
            purchase=self.purchase,
            book=self.book,
            quantity=2,
            unit_price=10.0,
            discount_percentage=5.0,
            total=19.0,
        )

        assert line.purchase == self.purchase.id
        assert line.book == self.book.get_descriptor()
        assert line.quantity == 2
        assert line.unit_price == 10.0
        assert line.discount_percentage == 5.0
        assert line.total == 19.0

    def test_should_run_modify(self):
        line = PurchaseLine.create(
            purchase=self.purchase,
            book=self.book,
            quantity=2,
            unit_price=10.0,
            discount_percentage=5.0,
            total=19.0,
        )

        new_book = BookMother.don_quijote()
        line.modify(
            book=new_book,
            quantity=3,
            unit_price=15.0,
            discount_percentage=10.0,
            total=40.5,
        )

        assert line.book == new_book.get_descriptor()
        assert line.quantity == 3
        assert line.unit_price == 15.0
        assert line.discount_percentage == 10.0
        assert line.total == 40.5
