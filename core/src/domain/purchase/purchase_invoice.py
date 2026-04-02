from dataclasses import dataclass

from src.domain.purchase.exception import InvalidPurchaseInvoiceNumberError


@dataclass
class PurchaseInvoice:
    """Represents a purchase invoice."""
    number: str = None
    amount: float = None
    taxes: float = None
    total: float = None

    @classmethod
    def create(
            cls,
            number: str,
            amount: float,
            taxes: float,
            total: float,
    ) -> "PurchaseInvoice":
        """
        Factory method to create a new PurchaseInvoice instance.
        """
        cls.check(number)

        return cls(number, amount, taxes, total)

    @staticmethod
    def check(number: str) -> None:
        """
        Validates the purchase invoice number.
        """
        if not number or not number.strip():
            raise InvalidPurchaseInvoiceNumberError()
