from datetime import datetime, timedelta

import pytest

from src.domain.sale import SaleInvoice
from src.domain.sale.exception import InvalidSaleDateError


class TestSaleInvoice:
    def test_should_fail_when_invalid_date(self):
        date = datetime.now() + timedelta(days=2)

        with pytest.raises(InvalidSaleDateError):
            SaleInvoice.create(date=date, amount=100, tax_percentage=10, taxes=10, total=110)

    def test_should_create(self):
        date = datetime.now()

        invoice = SaleInvoice.create(date=date, amount=100, tax_percentage=10, taxes=10, total=110)

        assert invoice.date == date
        assert invoice.amount == 100
        assert invoice.tax_percentage == 10
        assert invoice.taxes == 10
        assert invoice.total == 110
