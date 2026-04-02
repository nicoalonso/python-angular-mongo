from src.domain.book import BookRepository, Book, BookDescriptor
from src.domain.book.exception import BookNotFoundError
from src.domain.bus import DomainBus
from src.domain.customer import CustomerRepository, Customer
from src.domain.customer.exception import CustomerNotFoundError
from src.domain.sale import SaleRepository, SaleLineRepository, Sale, SaleInvoice, SaleLine
from src.domain.sale.exception import SaleLinesEmptyError
from src.domain.sequence import SequenceNumberRepository, SequenceType
from src.domain.user import UserRepository
from .payload import SaleInvoicePayload, SaleLinePayload
from .sale_create_payload import SaleCreatePayload
from .sale_created_event import SaleCreatedEvent


class SaleCreate:
    """
    Use case for creating a sale.

    :ivar repo_sale: Repository for sale data access.
    :ivar repo_sale_line: Repository for sale line data access.
    :ivar repo_customer: Repository for customer data access.
    :ivar repo_book: Repository for book data access.
    :ivar repo_sequence_number: Repository for sequence number management.
    :ivar repo_user: Repository for user data access.

    :ivar _book_cache: Cache for storing retrieved books to avoid redundant database calls.
    :ivar _book_list: Dictionary for storing book descriptors used in the purchase.
    """
    def __init__(
            self,
            repo_sale: SaleRepository,
            repo_sale_line: SaleLineRepository,
            repo_customer: CustomerRepository,
            repo_book: BookRepository,
            repo_sequence_number: SequenceNumberRepository,
            repo_user: UserRepository,
            bus: DomainBus,
    ):
        self.repo_sale = repo_sale
        self.repo_sale_line = repo_sale_line
        self.repo_customer = repo_customer
        self.repo_book = repo_book
        self.repo_sequence_number = repo_sequence_number
        self.repo_user = repo_user
        self.bus = bus

        self._book_cache: dict[str, Book] = {}
        self._book_list: dict[str, BookDescriptor] = {}

    async def dispatch(self, payload: SaleCreatePayload) -> Sale:
        """
        Create a new sale based on the provided payload.
        :param payload: Data required to create a new sale.
        :return: The created Sale object.
        """
        await self._check(payload)

        customer = await self._find_customer(payload.customer_id)
        invoice = self._make_invoice(payload.invoice)
        user = self.repo_user.obtain_user()

        number = await self._generate_invoice_next_number()

        sale = Sale.create(customer, number, invoice, user.name)
        await self.repo_sale.save(sale)

        await self._manage_lines(sale, payload.lines)

        books = list(self._book_list.values())
        event = SaleCreatedEvent(sale, books)
        await self.bus.dispatch(event)

        return sale

    async def _check(self, payload: SaleCreatePayload) -> None:
        """
        Check if the sale can be created based on the provided payload.
        :raises SaleLinesEmptyError: If the sale lines are empty.
        :raise BookNotFoundError: If any of the books in the sale lines are not found.
        """
        if len(payload.lines) == 0:
            raise SaleLinesEmptyError()

        # Check if the books already exists, to avoid later errors and rollbacks
        for line in payload.lines:
            await self._find_book(line.book_id)

    async def _find_customer(self, customer_id: str) -> Customer:
        """
        Find a customer by ID or Fail
        :raises CustomerNotFoundError: If the customer with the given ID is not found.
        """
        customer = await self.repo_customer.obtain_by_id(customer_id)
        if customer is None:
            raise CustomerNotFoundError(customer_id)

        return customer

    @staticmethod
    def _make_invoice(payload: SaleInvoicePayload) -> SaleInvoice:
        return SaleInvoice.create(
            date=payload.date,
            amount=payload.amount,
            tax_percentage=payload.tax_percentage,
            taxes=payload.taxes,
            total=payload.total,
        )

    async def _generate_invoice_next_number(self) -> str:
        """Generate the next invoice number for the sale."""
        while True:
            sequence_number = await self.repo_sequence_number.next_number(SequenceType.Sale)
            number = sequence_number.format()

            customer = await self.repo_sale.obtain_by_number(number)
            if customer is None:
                break

        return number

    async def _manage_lines(self, sale: Sale, lines: list[SaleLinePayload]) -> None:
        """Manage the sale lines for a given sale."""
        for line in lines:
            book = await self._find_book(line.book_id)
            self._add_book_descriptor(book.get_descriptor())

            sale_line = SaleLine.create(
                sale=sale,
                book=book,
                quantity=line.quantity,
                price=line.price,
                discount=line.discount,
                total=line.total,
            )
            await self.repo_sale_line.save(sale_line)

    async def _find_book(self, book_id: str) -> Book:
        """
        Find a book by ID or Fail
        :raises BookNotFoundError: If the book with the given ID is not found.
        """
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
