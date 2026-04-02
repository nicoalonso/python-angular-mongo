from dataclasses import dataclass

from src.domain.common import EnterpriseContact, Address
from src.domain.identity import Entity
from src.domain.identity.exception import NameEmptyError
from .editorial_descriptor import EditorialDescriptor


@dataclass
class Editorial(Entity):
    """
    Editorial entity represents a publishing house or editorial in the system.

    Attributes:
        name (str): The name of the editorial.
        comercial_name (str): The commercial name of the editorial.
        contact (EnterpriseContact): A dictionary containing contact information for the editorial.
        address (Address): A dictionary containing the address information for the editorial.
    """
    name: str = None
    comercial_name: str = None
    contact: EnterpriseContact = None
    address: Address = None

    @classmethod
    def create(
            cls,
            name: str,
            comercial_name: str,
            contact: EnterpriseContact,
            address: Address,
            created_by: str = None,
    ) -> "Editorial":
        """
        Factory method to create a new Editorial instance.
        """
        cls.check(name)

        return cls(
            name=name,
            comercial_name=comercial_name,
            contact=contact,
            address=address,
            created_by=created_by
        )

    def modify(
            self,
            name: str,
            comercial_name: str,
            contact: EnterpriseContact,
            address: Address,
            updated_by: str = None,
    ):
        self.check(name)

        self.name = name
        self.comercial_name = comercial_name
        self.contact = contact
        self.address = address
        self.updated(updated_by)

    @staticmethod
    def check(name: str) -> None:
        """
        Validates the input data for creating or updating an Editorial instance.

        :raises NameEmptyError: If the name is empty.
        """
        if not name:
            raise NameEmptyError()

    def get_descriptor(self) -> EditorialDescriptor:
        """
        Returns an EditorialDescriptor for this Editorial instance.
        """
        return EditorialDescriptor(
            id=self.id,
            name=self.name,
        )
