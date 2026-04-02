import pytest

from src.application.customer.reader import CustomerRead
from src.domain.customer.exception import CustomerNotFoundError
from tests.doubles.infrastructure.persistence import CustomerRepositoryStub
from tests.fixtures import Ref


class TestCustomerRead:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_customer = CustomerRepositoryStub()
        self.reader = CustomerRead(self.repo_customer)

    @pytest.mark.asyncio
    async def test_should_fail_when_not_found(self):
        with pytest.raises(CustomerNotFoundError):
            await self.reader.dispatch('not-exists-id')

    @pytest.mark.asyncio
    async def test_should_run_when_found(self):
        customer = self.repo_customer.put(Ref.CustomerJohnDoe)

        result = await self.reader.dispatch(customer.id)

        assert result is not None
        assert result.id == customer.id
