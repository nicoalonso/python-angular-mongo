from src.domain.purchase import PurchaseRepository, PurchaseLineRepository
from src.domain.purchase.exception import PurchaseNotFoundError
from .purchase_decorator import PurchaseDecorator


class PurchaseRead:
    """
    Use case for reading purchase information.

    :ivar repo_purchase: Repository for accessing purchase data.
    :ivar repo_purchase_line: Repository for accessing purchase line data.
    """
    def __init__(
            self,
            repo_purchase: PurchaseRepository,
            repo_purchase_line: PurchaseLineRepository,
    ):
        self.repo_purchase = repo_purchase
        self.repo_purchase_line = repo_purchase_line

    async def dispatch(self, purchase_id: str) -> PurchaseDecorator:
        """
        Dispatch the use case to read a purchase by its ID.

        :param purchase_id: The ID of the purchase to read.
        :return: A decorated purchase object containing the purchase and its lines.
        """
        purchase = await self.repo_purchase.obtain_by_id(purchase_id)
        if not purchase:
            raise PurchaseNotFoundError()

        lines = await self.repo_purchase_line.obtain_by_purchase(purchase_id)

        return PurchaseDecorator(purchase, lines)
