from src.domain.borrow import BorrowRepository
from src.domain.customer import CustomerRepository
from src.domain.customer.exception import CustomerNotFoundError
from src.domain.sale import SaleRepository
from .customer_associated_error import CustomerAssociatedError


class CustomerDelete:
    """
    Use case for deleting a customer.

    :ivar repo_customer: CustomerRepository - The repository for managing customer data.
    """
    def __init__(
            self,
            repo_customer: CustomerRepository,
            repo_sale: SaleRepository,
            repo_borrow: BorrowRepository,
    ):
        self.repo_customer = repo_customer
        self.repo_sale = repo_sale
        self.repo_borrow = repo_borrow

    async def dispatch(self, customer_id: str) -> None:
        """
        Deletes a customer by their ID.

        :param customer_id: str - The ID of the customer to delete.
        :raises NotFoundError: If the customer with the given ID does not exist.
        """
        customer = await self.repo_customer.obtain_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundError(customer_id)

        await self._check_associated(customer_id)

        await self.repo_customer.remove(customer.id)

    async def _check_associated(self, customer_id: str) -> None:
        borrows = await self.repo_borrow.obtain_by_customer(customer_id, 1)
        if not borrows.is_empty():
            raise CustomerAssociatedError('The customer is associated with one or more borrows.')

        sales = await self.repo_sale.obtain_by_customer(customer_id, 1)
        if not sales.is_empty():
            raise CustomerAssociatedError('The customer is associated with one or more sales.')
