from dataclasses import dataclass

from src.domain.common import EnterpriseContact, Address
from src.domain.identity import Entity
from src.domain.identity.exception import NameEmptyError
from .provider_descriptor import ProviderDescriptor


@dataclass
class Provider(Entity):
    """
    Provider entity represents a provider in the system.
    """
    name: str = None
    comercial_name: str = None
    contact: EnterpriseContact = None
    address: Address = None
    vat_number: str = None

    @classmethod
    def create(
            cls,
            name: str,
            comercial_name: str,
            contact: EnterpriseContact,
            address: Address,
            vat_number: str,
            created_by: str = None,
    ) -> "Provider":
        """
        Factory method to create a new Provider instance.
        """
        cls.check(name)

        return cls(
            name=name,
            comercial_name=comercial_name,
            contact=contact,
            address=address,
            vat_number=vat_number,
            created_by=created_by
        )

    def modify(
            self,
            name: str,
            comercial_name: str,
            contact: EnterpriseContact,
            address: Address,
            vat_number: str,
            updated_by: str = None,
    ):
        """
        Modifies the attributes of the Provider instance.
        """
        self.check(name)

        self.name = name
        self.comercial_name = comercial_name
        self.contact = contact
        self.address = address
        self.vat_number = vat_number
        self.updated(updated_by)

    @staticmethod
    def check(name: str) -> None:
        """
        Validates the name of the provider.

        :raises NameEmptyError: If the name is empty or consists only of whitespace.
        """
        if not name or name.strip() == "":
            raise NameEmptyError()

    def get_descriptor(self) -> ProviderDescriptor:
        """
        Returns a ProviderDescriptor for this Provider instance.
        """
        return ProviderDescriptor(
            id=self.id,
            name=self.name,
        )
