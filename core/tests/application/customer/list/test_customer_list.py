import pytest

from src.application.customer.list.customer_list import CustomerList
from src.domain.identity.list import ListQuery
from tests.doubles.infrastructure.persistence import CustomerRepositoryStub


class TestCustomerList:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_customer = CustomerRepositoryStub()
        self.lister = CustomerList(self.repo_customer)

    @pytest.mark.asyncio
    async def test_should_run_when_list(self):
        self.repo_customer.attach_all()

        query = ListQuery()
        result = await self.lister.dispatch(query)

        assert result.items.is_empty() is False
