from dataclasses import dataclass

from src.domain.customer import CustomerDescriptor, Customer
from src.domain.identity import Entity, Collection
from .exception import InvalidSaleInvoiceNumberError
from .sale_invoice import SaleInvoice


@dataclass
class Sale(Entity):
    """
    Represents a sale transaction in the system.
    """
    customer: CustomerDescriptor = None
    number: str = None
    invoice: SaleInvoice = None

    @classmethod
    def create(
            cls,
            customer: Customer,
            number: str,
            invoice: SaleInvoice,
            created_by: str,
    ) -> "Sale":
        """
        Factory method to create a new Sale instance.
        """
        cls.check(number)

        return cls(
            customer=customer.get_descriptor(),
            number=number,
            invoice=invoice,
            created_by=created_by,
        )

    @staticmethod
    def check(number: str):
        """
        Validates the sale
        :raises InvalidSaleInvoiceNumberError: If the invoice number is invalid (empty or whitespace).
        """
        if not number or not number.strip():
            raise InvalidSaleInvoiceNumberError()


type SaleCollection = Collection[Sale]
