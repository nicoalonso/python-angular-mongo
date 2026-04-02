import logging

from src.domain.book import BookRepository, BookDescriptor
from src.domain.book.exception import BookNotFoundError
from src.domain.purchase import PurchaseLineRepository
from src.domain.sale import SaleLineRepository


class BookInventory:
    """
    Use case for managing the inventory of books in a library or bookstore.

    :ivar _repo_book: Repository for accessing book data.
    :ivar _repo_purchase_line: Repository for accessing purchase line data.
    :ivar _repo_sale_line: Repository for accessing sale line data.
    :ivar _log: Logger for logging inventory operations.
    """
    def __init__(
            self,
            repo_book: BookRepository,
            repo_purchase_line: PurchaseLineRepository,
            repo_sale_line: SaleLineRepository,
    ):
        self._repo_book = repo_book
        self._repo_purchase_line = repo_purchase_line
        self._repo_sale_line = repo_sale_line
        self._log = logging.getLogger('uvicorn')

    async def dispatch(self, descriptor: BookDescriptor) -> None:
        """
        Calculate the current inventory of a book based on its descriptor.

        :param descriptor: The descriptor of the book to calculate inventory for.
        """
        self._log.info(f"Calculating inventory for book {descriptor.id}: {descriptor.title}")

        book = await self._get_book_or_fail(descriptor.id)
        stock = 0

        purchase_lines = await self._repo_purchase_line.obtain_by_book(book.id)
        self._log.info(f"Found {len(purchase_lines)} purchase lines for book {book.id}")

        for line in purchase_lines:
            stock += line.quantity

        sale_lines = await self._repo_sale_line.obtain_by_book(book.id)
        self._log.info(f"Found {len(sale_lines)} sale lines for book {book.id}")

        for line in sale_lines:
            stock -= line.quantity

        self._log.info(f"Calculated inventory for book {book.id}: {stock} units in stock")
        if stock < 0:
            self._log.warning(f"Inventory for book {book.id} is negative: {stock} units. Check for data inconsistencies.")
            stock = 0

        book.change_stock(stock)
        await self._repo_book.save(book)

    async def _get_book_or_fail(self, book_id: str):
        """Helper method to retrieve a book by its ID or raise an error if not found."""
        book = await self._repo_book.obtain_by_id(book_id)
        if not book:
            raise BookNotFoundError(book_id)
        return book
