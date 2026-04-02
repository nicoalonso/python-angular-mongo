import pytest

from src.application.customer.eraser import CustomerDelete, CustomerAssociatedError
from src.domain.customer.exception import CustomerNotFoundError
from tests.doubles.infrastructure.persistence import CustomerRepositoryStub, SaleRepositoryStub, BorrowRepositoryStub
from tests.fixtures import Ref


class TestCustomerDelete:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.repo_customer = CustomerRepositoryStub()
        self.repo_sale = SaleRepositoryStub(repo_customer=self.repo_customer)
        self.repo_borrow = BorrowRepositoryStub(repo_customer=self.repo_customer)
        self.eraser = CustomerDelete(
            repo_customer=self.repo_customer,
            repo_sale=self.repo_sale,
            repo_borrow=self.repo_borrow,
        )

    @pytest.mark.asyncio
    async def test_should_fail_when_not_found(self):
        with pytest.raises(CustomerNotFoundError):
            await self.eraser.dispatch("non-existent-id")

    @pytest.mark.asyncio
    async def test_should_fail_when_has_sales(self):
        self.repo_customer.put(Ref.CustomerJohnDoe)
        self.repo_sale.attach(Ref.SaleJohnDoe1)

        with pytest.raises(CustomerAssociatedError):
            await self.eraser.dispatch("customer-id")

    @pytest.mark.asyncio
    async def test_should_fail_when_has_borrows(self):
        self.repo_customer.put(Ref.CustomerJohnDoe)
        self.repo_borrow.attach(Ref.BorrowJohnDoe)

        with pytest.raises(CustomerAssociatedError):
            await self.eraser.dispatch("customer-id")

    @pytest.mark.asyncio
    async def test_should_delete_customer(self):
        self.repo_customer.put(Ref.CustomerJohnDoe)

        await self.eraser.dispatch('customer.id')

        assert self.repo_customer.removed is not None
