from src.application.purchase.creator import PurchaseMakeable
from src.domain.book import BookRepository
from src.domain.bus import DomainBus
from src.domain.provider import ProviderRepository
from src.domain.purchase import PurchaseRepository, PurchaseLineRepository, Purchase
from src.domain.purchase.exception import PurchaseNotFoundError
from src.domain.user import UserRepository
from .purchase_update_payload import PurchaseUpdatePayload
from .purchase_updated_event import PurchaseUpdatedEvent


class PurchaseUpdate(PurchaseMakeable):
    """
    Use case for updating a purchase.

    :ivar repo_purchase: Repository for managing purchases.
    :ivar repo_user: Repository for managing users.
    """
    def __init__(
            self,
            repo_purchase: PurchaseRepository,
            repo_purchase_line: PurchaseLineRepository,
            repo_provider: ProviderRepository,
            repo_book: BookRepository,
            repo_user: UserRepository,
            bus: DomainBus,
    ):
        super().__init__(repo_book, repo_provider, repo_purchase_line)

        self.repo_purchase = repo_purchase
        self.repo_user = repo_user
        self.bus = bus

    async def dispatch(self, purchase_id: str, payload: PurchaseUpdatePayload) -> Purchase:
        """
        Update an existing purchase based on the provided purchase ID and payload.

        :param purchase_id: The ID of the purchase to be updated.
        :param payload: (PurchaseUpdatePayload) Data required to update the purchase.
        :return: The updated Purchase object.
        """
        purchase = await self._get_purchase_or_fail(purchase_id)
        await self._check(payload)

        provider = await self._find_provider(payload.provider_id)
        invoice = self._make_invoice(payload.invoice)
        user = self.repo_user.obtain_user()

        purchase.modify(
            provider=provider,
            purchased_at=payload.purchased_at,
            invoice=invoice,
            updated_by=user.name,
        )

        current_lines = await self.repo_purchase_line.obtain_by_purchase(purchase_id)
        await self._manage_lines(purchase, payload.lines, current_lines)

        await self.repo_purchase.save(purchase)

        books = self._get_book_list()
        event = PurchaseUpdatedEvent(purchase, books)
        await self.bus.dispatch(event)

        return purchase

    async def _get_purchase_or_fail(self, purchase_id: str) -> Purchase:
        """
        Find a purchase by its ID or raise an error if it does not exist.

        :param purchase_id: The ID of the purchase to find.
        :return: The found Purchase object.
        """
        purchase = await self.repo_purchase.obtain_by_id(purchase_id)
        if not purchase:
            raise PurchaseNotFoundError(purchase_id)

        return purchase
