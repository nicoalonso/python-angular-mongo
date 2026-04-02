import pytest

from src.application.customer.updater import CustomerUpdate, CustomerUpdatePayload
from src.domain.customer.exception import CustomerNotFoundError
from tests.doubles.infrastructure.persistence import CustomerRepositoryStub, UserRepositoryStub
from tests.fixtures import FixturePayload, Ref


class TestCustomerUpdate:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_customer = CustomerRepositoryStub()
        repo_user = UserRepositoryStub()
        self.updater = CustomerUpdate(
            repo_customer=self.repo_customer,
            repo_user=repo_user,
        )

        loader = FixturePayload()
        data = loader.load('customer-update')
        self.payload = CustomerUpdatePayload(**data)

    @pytest.mark.asyncio
    async def test_should_fail_when_not_found(self):
        with pytest.raises(CustomerNotFoundError):
            await self.updater.dispatch('non-existent-id', self.payload)

    @pytest.mark.asyncio
    async def test_should_update_customer(self):
        self.repo_customer.put(Ref.CustomerJohnDoe)

        customer = await self.updater.dispatch('customer-id-1', self.payload)

        assert customer.name == self.payload.name
        assert self.repo_customer.stored is not None
