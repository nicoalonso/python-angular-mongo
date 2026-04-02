from dataclasses import dataclass
from datetime import datetime, timedelta

from src.domain.sale.exception import InvalidSaleDateError


@dataclass
class SaleInvoice:
    """Represents an invoice associated with a sale transaction."""
    date: datetime = None
    amount: float = None
    tax_percentage: float = None
    taxes: float = None
    total: float = None

    @classmethod
    def create(
            cls,
            date: datetime,
            amount: float,
            tax_percentage: float,
            taxes: float,
            total: float,
    ) -> "SaleInvoice":
        """
        Factory method to create a new SaleInvoice instance.
        """
        cls.check(date)

        return cls(date, amount, tax_percentage, taxes, total)

    @staticmethod
    def check(date: datetime) -> None:
        """
        Validates the sale invoice
        :raises InvalidSaleDateError: If the sale date is in the future
        """
        limit = datetime.now() + timedelta(days=1)

        if date > limit:
            raise InvalidSaleDateError()
