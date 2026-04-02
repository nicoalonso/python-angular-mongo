from typing import Optional

from src.domain.sale import Sale, SaleRepository, SaleCollection
from tests.fixtures import Ref
from tests.fixtures.mothers import SaleMother
from .entity_repository_stub import EntityRepositoryStub
from .customer_repository_stub import CustomerRepositoryStub


class SaleRepositoryStub(EntityRepositoryStub[Sale], SaleRepository):
    """
    Stub implementation of the SaleRepository for testing purposes.
    """
    def __init__(
            self,
            *,
            repo_customer: Optional[CustomerRepositoryStub] = None,
    ):
        self.repo_customer = repo_customer

        super().__init__()

    async def obtain_by_number(self, number: str) -> Sale | None:
        self.query_filter = number
        self._throw_error()
        return self.read

    async def obtain_by_customer(self, customer_id: str, limit: int | None = None) -> SaleCollection:
        self.query_filter = (customer_id, limit)
        self._throw_error()
        return self.list

    def make_fixtures(self) -> None:
        john_doe = None

        if self.repo_customer:
            john_doe = self.repo_customer.get(Ref.CustomerJohnDoe)

        john_doe_sale1 = SaleMother.john_doe_sale1(customer=john_doe)
        self.add_fixture(Ref.SaleJohnDoe1, john_doe_sale1)

        john_doe_sale2 = SaleMother.john_doe_sale2(customer=john_doe)
        self.add_fixture(Ref.SaleJohnDoe2, john_doe_sale2)
