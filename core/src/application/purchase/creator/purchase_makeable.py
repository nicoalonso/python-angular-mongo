from abc import ABC
from typing import Optional

from src.application.purchase.creator.payload import PurchaseInvoicePayload, PurchaseLinePayload
from src.domain.book import BookRepository, Book, BookDescriptor
from src.domain.book.exception import BookNotFoundError
from src.domain.identity import Collection
from src.domain.provider import ProviderRepository, Provider
from src.domain.provider.exception import ProviderNotFoundError
from src.domain.purchase import PurchaseLineRepository, PurchaseInvoice, Purchase, PurchaseLineCollection, PurchaseLine
from .purchase_create_payload import PurchaseCreatePayload


class PurchaseMakeable(ABC):
    """
    Abstract class for purchase creation.

    :ivar repo_book: Repository for managing books.
    :ivar repo_provider: Repository for managing providers.
    :ivar repo_purchase_line: Repository for managing purchase lines.

    :ivar _book_cache: Cache for storing retrieved books to avoid redundant database calls.
    :ivar _book_list: Dictionary for storing book descriptors used in the purchase.
    """
    def __init__(
            self,
            repo_book: BookRepository,
            repo_provider: ProviderRepository,
            repo_purchase_line: PurchaseLineRepository,
    ):
        self.repo_book = repo_book
        self.repo_provider = repo_provider
        self.repo_purchase_line = repo_purchase_line

        self._book_cache: dict[str, Book] = {}
        self._book_list: dict[str, BookDescriptor] = {}

    async def _check(self, payload: PurchaseCreatePayload) -> None:
        """Check if the purchase can be created based on the provided payload."""
        # Check if the books already exists, to avoid later erros and rollbacks
        for line in payload.lines:
            await self._find_book(line.book_id)

    async def _find_provider(self, provider_id: str) -> Provider:
        """Find a provider by ID or Fail"""
        provider = await self.repo_provider.obtain_by_id(provider_id)
        if provider is None:
            raise ProviderNotFoundError(provider_id)

        return provider

    @staticmethod
    def _make_invoice(payload: PurchaseInvoicePayload) -> PurchaseInvoice:
        return PurchaseInvoice.create(
            number=payload.number,
            amount=payload.amount,
            taxes=payload.taxes,
            total=payload.total,
        )

    async def _manage_lines(
            self,
            purchase: Purchase,
            lines: list[PurchaseLinePayload],
            current: Optional[PurchaseLineCollection] = None
    ) -> None:
        if not current:
            current = Collection()

        for line in lines:
            book = await self._find_book(line.book_id)
            self._add_book_descriptor(book.get_descriptor())

            purchase_line = current.find_first(lambda l: l.id == line.line_id)
            if purchase_line is None:
                purchase_line = PurchaseLine.create(
                    purchase=purchase,
                    book=book,
                    quantity=line.quantity,
                    unit_price=line.unit_price,
                    discount_percentage=line.discount_percentage,
                    total=line.total,
                )
            else:
                current.remove(purchase_line)

                purchase_line.modify(
                    book=book,
                    quantity=line.quantity,
                    unit_price=line.unit_price,
                    discount_percentage=line.discount_percentage,
                    total=line.total,
                )

            await self.repo_purchase_line.save(purchase_line)

        for line in current:
            self._add_book_descriptor(line.book)
            await self.repo_purchase_line.remove(line.id)

    async def _find_book(self, book_id: str) -> Book:
        """Find a book by ID or Fail"""
        if book_id in self._book_cache:
            return self._book_cache[book_id]

        book = await self.repo_book.obtain_by_id(book_id)
        if book is None:
            raise BookNotFoundError(book_id)

        self._book_cache[book_id] = book
        return book

    def _add_book_descriptor(self, descriptor: BookDescriptor) -> None:
        """Add a book descriptor to the list if it doesn't already exist."""
        if not descriptor.id in self._book_list:
            self._book_list[descriptor.id] = descriptor

    def _get_book_list(self) -> list[BookDescriptor]:
        """Get the list of book descriptors for the purchase."""
        return list(self._book_list.values())
