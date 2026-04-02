import pytest

from src.application.purchase.reader.purchase_read import PurchaseRead
from src.domain.purchase.exception import PurchaseNotFoundError
from tests.doubles.infrastructure.persistence import PurchaseRepositoryStub, PurchaseLineRepositoryStub
from tests.fixtures import Ref


class TestPurchaseRead:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_purchase = PurchaseRepositoryStub()
        self.repo_purchase_line = PurchaseLineRepositoryStub(repo_purchase=self.repo_purchase)
        self.reader = PurchaseRead(self.repo_purchase, self.repo_purchase_line)

    @pytest.mark.asyncio
    async def test_should_fail_when_not_found(self):
        with pytest.raises(PurchaseNotFoundError):
            await self.reader.dispatch('not-exists-id')

    @pytest.mark.asyncio
    async def test_should_run_when_found(self):
        purchase = self.repo_purchase.put(Ref.PurchaseAmazonInv1)
        self.repo_purchase_line.attach(Ref.PurchaseLineAmazonLine1)

        result = await self.reader.dispatch(purchase.id)

        assert result.id == purchase.id
        assert result.get_lines().count() == 1
