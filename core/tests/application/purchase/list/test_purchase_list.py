import pytest

from src.application.purchase.list import PurchaseList
from src.domain.identity.list import ListQuery
from tests.doubles.infrastructure.persistence import PurchaseRepositoryStub


class TestPurchaseList:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_purchase = PurchaseRepositoryStub()
        self.lister = PurchaseList(self.repo_purchase)

    @pytest.mark.asyncio
    async def test_should_run_when_list(self):
        self.repo_purchase.attach_all()

        query = ListQuery()
        result = await self.lister.dispatch(query)

        assert result.items.is_empty() is False
