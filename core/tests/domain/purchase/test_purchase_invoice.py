import pytest

from src.domain.purchase.exception import InvalidPurchaseInvoiceNumberError
from src.domain.purchase import PurchaseInvoice


class TestPurchaseInvoice:
    def test_should_fail_when_number_is_empty(self):
        with pytest.raises(InvalidPurchaseInvoiceNumberError) as exc:
            PurchaseInvoice.create(
                number='',
                amount=100.0,
                taxes=20.0,
                total=120.0
            )

        assert str(exc.value) == 'The purchase invoice number is required.'

    def test_should_create(self):
        invoice = PurchaseInvoice.create(
            number='INV-001',
            amount=100.0,
            taxes=20.0,
            total=120.0
        )

        assert invoice.number == 'INV-001'
        assert invoice.amount == 100.0
        assert invoice.taxes == 20.0
        assert invoice.total == 120.0
