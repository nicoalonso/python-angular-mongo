from typing import Optional

from src.domain.borrow import Borrow, BorrowRepository
from src.domain.borrow.borrow import BorrowCollection
from tests.fixtures import Ref
from tests.fixtures.mothers import BorrowMother
from .entity_repository_stub import EntityRepositoryStub
from .customer_repository_stub import CustomerRepositoryStub


class BorrowRepositoryStub(EntityRepositoryStub[Borrow], BorrowRepository):
    """
    Stub implementation of the BorrowRepository for testing purposes.
    """
    def __init__(
            self,
            *,
            repo_customer: Optional[CustomerRepositoryStub] = None,
    ):
        self.repo_customer = repo_customer

        super().__init__()

    async def obtain_by_number(self, number: str) -> Borrow | None:
        self.query_filter = number
        self._throw_error()
        return self.read

    async def obtain_by_customer(self, customer_id: str, limit: int | None = None) -> BorrowCollection:
        self.query_filter = (customer_id, limit)
        self._throw_error()
        return self.list

    async def obtain_by_overdue(self) -> BorrowCollection:
        self._throw_error()
        return self.list

    def make_fixtures(self) -> None:
        john_doe = None

        if self.repo_customer:
            john_doe = self.repo_customer.get(Ref.CustomerJohnDoe)

        borrow_john_doe = BorrowMother.john_doe(customer=john_doe)
        self.add_fixture(Ref.BorrowJohnDoe, borrow_john_doe)
