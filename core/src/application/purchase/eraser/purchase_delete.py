from src.domain.bus import DomainBus
from src.domain.purchase import PurchaseRepository, PurchaseLineRepository
from src.domain.purchase.exception import PurchaseNotFoundError
from .purchase_deleted_event import PurchaseDeletedEvent


class PurchaseDelete:
    """
    Use case for deleting a purchase.

    :ivar repo_purchase: Repository for managing purchases.
    :ivar repo_purchase_line: Repository for managing purchase lines.
    """
    def __init__(
            self,
            repo_purchase: PurchaseRepository,
            repo_purchase_line: PurchaseLineRepository,
            bus: DomainBus,
    ):
        self.repo_purchase = repo_purchase
        self.repo_purchase_line = repo_purchase_line
        self.bus = bus

    async def dispatch(self, purchase_id: str) -> None:
        """
        Deletes a purchase and its associated purchase lines.

        :param purchase_id: The ID of the purchase to delete.
        """
        purchase = await self.repo_purchase.obtain_by_id(purchase_id)
        if purchase is None:
            raise PurchaseNotFoundError()

        lines = await self.repo_purchase_line.obtain_by_purchase(purchase_id)
        for line in lines:
            await self.repo_purchase_line.remove(line.id)

        await self.repo_purchase.remove(purchase_id)

        books = lines.map(lambda l: l.book).to_array()
        event = PurchaseDeletedEvent(purchase, books)
        await self.bus.dispatch(event)
