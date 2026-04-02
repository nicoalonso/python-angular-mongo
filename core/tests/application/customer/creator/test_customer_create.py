import pytest

from src.application.customer.creator import CustomerCreate, CustomerCreatePayload
from src.domain.customer.exception import CustomerAlreadyExistsError
from tests.doubles.infrastructure.persistence import CustomerRepositoryStub, SequenceNumberRepositoryStub, \
    UserRepositoryStub
from tests.fixtures import FixturePayload, Ref


class TestCustomerCreate:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_customer = CustomerRepositoryStub()
        repo_sequence = SequenceNumberRepositoryStub()
        repo_user = UserRepositoryStub()
        self.creator = CustomerCreate(
            repo_customer=self.repo_customer,
            repo_sequence_number=repo_sequence,
            repo_user=repo_user,
        )

        loader = FixturePayload()
        data = loader.load('customer-create')
        self.payload = CustomerCreatePayload(**data)

    @pytest.mark.asyncio
    async def test_should_fail_when_already_exists(self):
        self.repo_customer.put(Ref.CustomerJohnDoe)

        with pytest.raises(CustomerAlreadyExistsError):
            await self.creator.dispatch(self.payload)

    @pytest.mark.asyncio
    async def test_should_create_customer(self):
        customer = await self.creator.dispatch(self.payload)

        assert customer.name == self.payload.name
        assert customer.membership.number == "SN00002"
        assert self.repo_customer.stored is not None
