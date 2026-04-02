from dataclasses import dataclass
from datetime import datetime, timedelta

from src.domain.identity import Entity, Collection
from src.domain.provider import ProviderDescriptor, Provider
from .exception import InvalidPurchaseDateError
from .purchase_invoice import PurchaseInvoice


@dataclass
class Purchase(Entity):
    """
    Purchase entity represents a purchase made by a user in the system.
    """
    provider: ProviderDescriptor = None
    purchased_at: datetime = None
    invoice: PurchaseInvoice = None

    @classmethod
    def create(
            cls,
            provider: Provider,
            purchased_at: datetime,
            invoice: PurchaseInvoice,
            created_by: str,
    ) -> "Purchase":
        """
        Factory method to create a new Purchase instance.
        """
        cls.check(purchased_at)

        return cls(
            provider=provider.get_descriptor(),
            purchased_at=purchased_at,
            invoice=invoice,
            created_by=created_by,
        )

    def modify(
            self,
            provider: Provider,
            purchased_at: datetime,
            invoice: PurchaseInvoice,
            updated_by: str,
    ) -> None:
        """
        Method to modify the purchase details.
        """
        self.check(purchased_at)

        self.provider = provider.get_descriptor()
        self.purchased_at = purchased_at
        self.invoice = invoice
        self.updated(updated_by)

    @staticmethod
    def check(purchased_at: datetime) -> None:
        """
        Validates the purchase date.
        """
        limit = datetime.now() + timedelta(days=1)

        if purchased_at > limit:
            raise InvalidPurchaseDateError()


type PurchaseCollection = Collection[Purchase]
