from dataclasses import dataclass

from src.domain.common import Address
from src.domain.identity import Entity
from src.domain.identity.exception import NameEmptyError
from .contact_info import ContactInfo
from .customer_descriptor import CustomerDescriptor
from .membership import Membership


@dataclass
class Customer(Entity):
    """
    Customer entity represents a customer in the system.
    """
    name: str = None
    surname: str = None
    membership: Membership = None
    contact: ContactInfo = None
    address: Address = None
    vat_number: str = None

    @classmethod
    def create(
            cls,
            name: str,
            surname: str,
            membership: Membership,
            contact: ContactInfo,
            address: Address,
            vat_number: str,
            created_by: str = None
    ) -> "Customer":
        """
        Factory method to create a new Customer instance.
        """
        cls._check(name)

        return cls(
            name=name,
            surname=surname,
            membership=membership,
            contact=contact,
            address=address,
            vat_number=vat_number,
            created_by=created_by
        )

    def modify(
            self,
            name: str,
            surname: str,
            contact: ContactInfo,
            address: Address,
            vat_number: str,
            active: bool,
            updated_by: str
    ) -> None:
        """
        Modifies the attributes of the Customer instance.
        """
        self._check(name)

        self.name = name
        self.surname = surname
        self.contact = contact
        self.address = address
        self.vat_number = vat_number

        if active:
            self.membership.enable()
        else:
            self.membership.disable()

        self.updated(updated_by)

    @staticmethod
    def _check(name: str):
        """
        Validates the name of the customer.

        :raises NameEmptyError: If the name is empty or consists only of whitespace.
        """
        if not name or name.strip() == "":
            raise NameEmptyError()

    def get_descriptor(self) -> CustomerDescriptor:
        """
        Returns a descriptor object containing the attributes of the Customer instance.
        """
        return CustomerDescriptor(
            id=self.id,
            name=self.name,
            surname=self.surname,
            vat_number=self.vat_number,
            number=self.membership.number if self.membership else None
        )
