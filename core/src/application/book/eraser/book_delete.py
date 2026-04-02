from src.domain.book import BookRepository
from src.domain.book.exception import BookNotFoundError
from src.domain.borrow import BorrowLineRepository
from src.domain.purchase import PurchaseLineRepository
from src.domain.sale import SaleLineRepository
from .book_associated_error import BookAssociatedError


class BookDelete:
    """
    Use case for deleting a book from the system.

    :ivar repo_book: The repository for managing book data.
    """
    def __init__(
            self,
            repo_book: BookRepository,
            repo_purchase_line: PurchaseLineRepository,
            repo_sale_line: SaleLineRepository,
            repo_borrow_line: BorrowLineRepository
    ):
        self.repo_book = repo_book
        self.repo_purchase_line = repo_purchase_line
        self.repo_sale_line = repo_sale_line
        self.repo_borrow_line = repo_borrow_line

    async def dispatch(self, book_id: str) -> None:
        """
        Deletes a book by its ID.

        :param book_id: The ID of the book to delete.
        """
        book = await self.repo_book.obtain_by_id(book_id)
        if not book:
            raise BookNotFoundError(book_id)

        await self._check_associated(book_id)

        await self.repo_book.remove(book.id)

    async def _check_associated(self, book_id: str) -> None:
        """
        Checks if the book has associated sales or details that would prevent deletion.

        :param book_id: The ID of the book to check.
        """
        purchase_lines = await self.repo_purchase_line.obtain_by_book(book_id, 1)
        if not purchase_lines.is_empty():
            raise BookAssociatedError()

        borrow_lines = await self.repo_borrow_line.obtain_by_book(book_id, 1)
        if not borrow_lines.is_empty():
            raise BookAssociatedError("Cannot delete book with associated borrow lines.")

        sale_lines = await self.repo_sale_line.obtain_by_book(book_id, 1)
        if not sale_lines.is_empty():
            raise BookAssociatedError("Cannot delete book with associated sale lines.")
