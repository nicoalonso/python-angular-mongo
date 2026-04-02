from src.domain.customer import Customer, CustomerRepository
from tests.fixtures import Ref
from tests.fixtures.mothers import CustomerMother
from .entity_repository_stub import EntityRepositoryStub


class CustomerRepositoryStub(EntityRepositoryStub[Customer], CustomerRepository):
    """
    A stub for the CustomerRepository interface used in tests.
    """

    async def obtain_by_name(self, name: str, surname: str) -> Customer | None:
        self.query_filter = (name, surname)
        self._throw_error()
        return self.read

    async def obtain_by_number(self, number: str) -> Customer | None:
        self.query_filter = number
        self._throw_error()
        return self.read

    def make_fixtures(self) -> None:
        john_doe = CustomerMother.john_doe()
        self.add_fixture(Ref.CustomerJohnDoe, john_doe)
