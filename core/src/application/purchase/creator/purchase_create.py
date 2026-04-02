from src.domain.book import BookRepository
from src.domain.bus import DomainBus
from src.domain.provider import ProviderRepository
from src.domain.purchase import Purchase, PurchaseRepository, PurchaseLineRepository
from src.domain.purchase.exception import PurchaseAlreadyExistsError
from src.domain.user import UserRepository
from .purchase_create_payload import PurchaseCreatePayload
from .purchase_makeable import PurchaseMakeable
from .purchase_created_event import PurchaseCreatedEvent


class PurchaseCreate(PurchaseMakeable):
    """
    Use class for creating a purchase.

    :ivar repo_purchase: Repository for purchase data access.
    :ivar repo_user: Repository for user data access.
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

    async def dispatch(self, payload: PurchaseCreatePayload) -> Purchase:
        """
        Create a new purchase based on the provided payload.

        :param payload: Data required to create a new purchase.
        :return: The created Purchase object.
        """
        await self._check(payload)
        await self._check_already_exists(payload)

        provider = await self._find_provider(payload.provider_id)
        invoice = self._make_invoice(payload.invoice)
        user = self.repo_user.obtain_user()

        purchase = Purchase.create(
            provider=provider,
            purchased_at=payload.purchased_at,
            invoice=invoice,
            created_by=user.name,
        )
        await self.repo_purchase.save(purchase)

        await self._manage_lines(purchase, payload.lines)

        books = self._get_book_list()
        event = PurchaseCreatedEvent(purchase, books)
        await self.bus.dispatch(event)

        return purchase

    async def _check_already_exists(self, payload: PurchaseCreatePayload) -> None:
        purchase = await self.repo_purchase.obtain_by_provider_and_number(
            payload.provider_id,
            payload.invoice.number
        )
        if purchase is not None:
            raise PurchaseAlreadyExistsError()
