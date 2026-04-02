from src.domain.common import Address
from src.domain.customer import CustomerRepository, Customer, Membership, ContactInfo
from src.domain.customer.exception import CustomerAlreadyExistsError
from src.domain.sequence import SequenceNumberRepository, SequenceType
from src.domain.user import UserRepository
from .customer_create_payload import CustomerCreatePayload


class CustomerCreate:
    """
    Use case for creating a new customer.

    :ivar repo_customer: Repository for customer data access.
    :ivar repo_sequence_number: Repository for managing sequence numbers.
    :ivar repo_user: Repository for user data access.
    """
    def __init__(
            self,
            repo_customer: CustomerRepository,
            repo_sequence_number: SequenceNumberRepository,
            repo_user: UserRepository,
    ):
        self.repo_customer = repo_customer
        self.repo_sequence_number = repo_sequence_number
        self.repo_user = repo_user

    async def dispatch(self, payload: CustomerCreatePayload) -> Customer:
        """
        Create a new customer based on the provided payload.
        :param payload: Data required to create a new customer.
        :return: The created Customer object.
        """
        await self._check_already_exists(payload)

        number = await self._generate_membership_next_number()
        membership = Membership.create(number)

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
        user = self.repo_user.obtain_user()

        customer = Customer.create(
            name=payload.name,
            surname=payload.surname,
            membership=membership,
            contact=contact,
            address=address,
            vat_number=payload.vat_number,
            created_by=user.name,
        )
        await self.repo_customer.save(customer)
        return customer

    async def _check_already_exists(self, payload):
        """Check if a customer with the same name already exists."""
        customer = await self.repo_customer.obtain_by_name(payload.name, payload.surname)
        if customer is not None:
            raise CustomerAlreadyExistsError()

    async def _generate_membership_next_number(self) -> str:
        """Generate the next membership number using the sequence number repository."""
        while True:
            sequence_number = await self.repo_sequence_number.next_number(SequenceType.Membership)
            number = sequence_number.format()

            customer = await self.repo_customer.obtain_by_number(number)
            if customer is None:
                 break

        return number
