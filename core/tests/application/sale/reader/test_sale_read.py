import pytest

from src.application.sale.reader.sale_read import SaleRead
from src.domain.sale.exception import SaleNotFoundError
from tests.doubles.infrastructure.persistence import SaleRepositoryStub, SaleLineRepositoryStub
from tests.fixtures import Ref


class TestSaleRead:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_sale = SaleRepositoryStub()
        self.repo_sale_line = SaleLineRepositoryStub(repo_sale=self.repo_sale)
        self.reader = SaleRead(self.repo_sale, self.repo_sale_line)

    @pytest.mark.asyncio
    async def test_should_fail_when_not_found(self):
        with pytest.raises(SaleNotFoundError):
            await self.reader.dispatch('not-exists-id')

    @pytest.mark.asyncio
    async def test_should_run_when_found(self):
        sale = self.repo_sale.put(Ref.SaleJohnDoe1)
        self.repo_sale_line.attach(Ref.SaleLineJohnDoe1Line1)

        result = await self.reader.dispatch(sale.id)

        assert result.id == sale.id
        assert result.get_lines().count() == 1
