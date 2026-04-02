from src.domain.common import Address
from src.domain.customer import CustomerRepository, Customer, ContactInfo
from src.domain.customer.exception import CustomerNotFoundError
from src.domain.user import UserRepository
from .customer_update_payload import CustomerUpdatePayload


class CustomerUpdate:
    """
    Use case for updating a customer.

    :ivar repo_customer: CustomerRepository - The repository for managing customer data.
    :ivar repo_user: UserRepository - The repository for managing user data
    """
    def __init__(
            self,
            repo_customer: CustomerRepository,
            repo_user: UserRepository,
    ):
        self.repo_customer = repo_customer
        self.repo_user = repo_user

    async def dispatch(self, customer_id: str, payload: CustomerUpdatePayload) -> Customer:
        """
        Update a customer
        :param customer_id: The ID of the customer to be updated
        :param payload: The data for updating the customer
        :return: The updated customer
        """
        customer = await self.repo_customer.obtain_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundError(customer_id)

        user = self.repo_user.obtain_user()
        contact = ContactInfo(
            email=payload.contact.email or "",
            phone1=payload.contact.phone1,
            phone2=payload.contact.phone2,
        )
        address = Address(
            street=payload.address.street,
            postal_code=payload.address.postal_code,
            city=payload.address.city,
            province=payload.address.province,
            country=payload.address.country,
        )

        print('Updating customer with ID:', payload)
        customer.modify(
            name=payload.name,
            surname=payload.surname,
            contact=contact,
            address=address,
            vat_number=payload.vat_number,
            active=payload.membership.active,
            updated_by=user.name,
        )

        await self.repo_customer.save(customer)
        return customer
