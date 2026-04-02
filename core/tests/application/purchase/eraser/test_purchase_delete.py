import pytest

from src.application.purchase.eraser import PurchaseDelete
from src.application.purchase.eraser.purchase_deleted_event import PurchaseDeletedEvent
from src.domain.purchase.exception import PurchaseNotFoundError
from tests.doubles.infrastructure.bus import DomainBusStub, assert_dispatch
from tests.doubles.infrastructure.persistence import PurchaseRepositoryStub, PurchaseLineRepositoryStub
from tests.fixtures import Ref


class TestPurchaseDelete:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_purchase = PurchaseRepositoryStub()
        self.repo_purchase_line = PurchaseLineRepositoryStub(
            repo_purchase=self.repo_purchase,
        )
        self.bus = DomainBusStub()
        self.eraser = PurchaseDelete(
            repo_purchase=self.repo_purchase,
            repo_purchase_line=self.repo_purchase_line,
            bus=self.bus,
        )

    @pytest.mark.asyncio
    async def test_should_fail_when_not_found(self):
        with pytest.raises(PurchaseNotFoundError) as exc:
            await self.eraser.dispatch('non-existent-id')

        assert str(exc.value) == 'The purchase was not found.'

    @pytest.mark.asyncio
    async def test_should_delete_purchase_and_lines(self):
        purchase = self.repo_purchase.put(Ref.PurchaseAmazonInv1)
        self.repo_purchase_line.attach(Ref.PurchaseLineAmazonLine1)
        self.repo_purchase_line.attach(Ref.PurchaseLineAmazonLine2)

        await self.eraser.dispatch(purchase.id)

        assert self.repo_purchase.removed is not None
        assert self.repo_purchase_line.removed is not None
        assert_dispatch(self.bus, PurchaseDeletedEvent)
