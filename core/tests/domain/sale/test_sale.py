import pytest

from src.domain.sale import Sale
from src.domain.sale.exception import InvalidSaleInvoiceNumberError
from tests.fixtures.mothers import CustomerMother, SaleInvoiceMother


class TestSale:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.customer = CustomerMother.john_doe()
        self.invoice = SaleInvoiceMother.john_doe_sale1()

    def test_fail_when_number_empty(self):
        with pytest.raises(InvalidSaleInvoiceNumberError):
            Sale.create(
                self.customer,
                '',
                self.invoice,
                'me',
            )

    def test_should_create(self):
        sale = Sale.create(
            self.customer,
            'INV-001',
            self.invoice,
            'me',
        )

        assert sale.customer == self.customer.get_descriptor()
        assert sale.number == 'INV-001'
        assert sale.invoice == self.invoice
