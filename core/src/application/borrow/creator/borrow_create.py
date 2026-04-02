from src.domain.book import Book, BookRepository
from src.domain.book.exception import BookNotFoundError
from src.domain.borrow import BorrowRepository, BorrowLineRepository, Borrow, BorrowLine
from src.domain.borrow.exception import BorrowLinesEmptyError
from src.domain.customer import CustomerRepository, Customer
from src.domain.customer.exception import CustomerNotFoundError
from src.domain.sequence import SequenceNumberRepository, SequenceType
from src.domain.user import UserRepository
from .borrow_create_payload import BorrowCreatePayload
from .payload import BorrowLinePayload


class BorrowCreate:
    """
    Use case for create a borrow.

    :ivar repo_borrow: Repository for managing borrows.
    :ivar repo_borrow_line: Repository for managing borrow lines.
    :ivar repo_customer: Repository for managing customers.
    :ivar repo_book: Repository for managing books.
    :ivar repo_sequence_number: Repository for managing sequence numbers.
    :ivar repo_user: Repository for managing users.
    """
    def __init__(
            self,
            repo_borrow: BorrowRepository,
            repo_borrow_line: BorrowLineRepository,
            repo_customer: CustomerRepository,
            repo_book: BookRepository,
            repo_sequence_number: SequenceNumberRepository,
            repo_user: UserRepository,
    ):
        self.repo_borrow = repo_borrow
        self.repo_borrow_line = repo_borrow_line
        self.repo_customer = repo_customer
        self.repo_book = repo_book
        self.repo_sequence_number = repo_sequence_number
        self.repo_user = repo_user

        self._book_cache: dict[str, Book] = {}

    async def dispatch(self, payload: BorrowCreatePayload) -> Borrow:
        """
        Create a new borrow based on the provided payload.
        :param payload: Data required to create a new borrow.
        :return: The created Borrow object.
        """
        await self._check(payload)

        customer = await self._find_customer(payload.customer_id)
        user = self.repo_user.obtain_user()

        number = await self._generate_borrow_next_number()

        borrow = Borrow.create(
            customer,
            number,
            len(payload.lines),
            user.name,
        )
        await self.repo_borrow.save(borrow)

        await self._manage_lines(borrow, payload.lines)

        return borrow

    async def _check(self, payload: BorrowCreatePayload) -> None:
        """
        Check if the borrow can be created based on the provided payload.

        :raises BorrowLinesEmptyError: If the borrow lines are empty.
        :raises BookNotFoundError: If the book with the given ID is not found.
        """
        if len(payload.lines) == 0:
            raise BorrowLinesEmptyError()

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

    async def _generate_borrow_next_number(self) -> str:
        """Generate the next invoice number for the sale."""
        while True:
            sequence_number = await self.repo_sequence_number.next_number(SequenceType.Borrow)
            number = sequence_number.format()

            customer = await self.repo_borrow.obtain_by_number(number)
            if customer is None:
                break

        return number

    async def _manage_lines(self, borrow: Borrow, lines: list[BorrowLinePayload]) -> None:
        """Manage the borrow lines for a given borrow."""
        for line in lines:
            book = await self._find_book(line.book_id)
            borrow_line = BorrowLine.create(borrow=borrow, book=book)
            await self.repo_borrow_line.save(borrow_line)

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
