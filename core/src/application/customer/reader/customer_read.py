from src.domain.customer import CustomerRepository, Customer
from src.domain.customer.exception import CustomerNotFoundError


class CustomerRead:
    """
    Use case for reading customer information.

    :ivar repo_customer: CustomerRepository - Repository for accessing customer data.
    """
    def __init__(self, repo_customer: CustomerRepository):
        self.repo_customer = repo_customer

    async def dispatch(self, customer_id: str) -> Customer:
        """
        Retrieves a customer by their ID.

        :param customer_id: str - The ID of the customer to retrieve.
        :return: Customer - The customer instance corresponding to the provided ID.
        """
        customer = await self.repo_customer.obtain_by_id(customer_id)
        if customer is None:
            raise CustomerNotFoundError(customer_id)

        return customer
