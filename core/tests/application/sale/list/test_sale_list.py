import pytest

from src.application.sale.list import SaleList
from src.domain.identity.list import ListQuery
from tests.doubles.infrastructure.persistence import SaleRepositoryStub


class TestSaleList:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_sale = SaleRepositoryStub()
        self.lister = SaleList(self.repo_sale)

    @pytest.mark.asyncio
    async def test_should_run_when_list(self):
        self.repo_sale.attach_all()

        query = ListQuery()
        result = await self.lister.dispatch(query)

        assert result.items.is_empty() is False
