from datetime import datetime, timedelta

import pytest

from src.domain.purchase import Purchase
from src.domain.purchase.exception import InvalidPurchaseDateError
from tests.fixtures.mothers import ProviderMother, PurchaseInvoiceMother


class TestPurchase:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.invoice = PurchaseInvoiceMother.invoice1()
        self.provider = ProviderMother.best_buy()

    def test_should_fail_when_purchase_at_is_in_future(self):
        date = datetime.now() + timedelta(days=2)

        with pytest.raises(InvalidPurchaseDateError):
            Purchase.create(
                provider=self.provider,
                purchased_at=date,
                invoice=self.invoice,
                created_by='test_user',
            )

    def test_should_create_purchase(self):
        date = datetime.now()

        purchase = Purchase.create(
            provider=self.provider,
            purchased_at=date,
            invoice=self.invoice,
            created_by='test_user',
        )

        assert purchase.provider == self.provider.get_descriptor()
        assert purchase.purchased_at == date
        assert purchase.invoice == self.invoice

    def test_should_modify_purchase(self):
        date = datetime.now()
        purchase = Purchase.create(
            provider=self.provider,
            purchased_at=date,
            invoice=self.invoice,
            created_by='test_user',
        )

        new_date = datetime.now() - timedelta(days=1)
        new_invoice = PurchaseInvoiceMother.invoice2()
        purchase.modify(
            provider=self.provider,
            purchased_at=new_date,
            invoice=new_invoice,
            updated_by='test_user',
        )

        assert purchase.provider == self.provider.get_descriptor()
        assert purchase.purchased_at == new_date
        assert purchase.invoice == new_invoice
