from src.domain.borrow import BorrowLineRepository
from .book_borrow_inspect import BookBorrowInspect
from .book_inspector import BookInspector
from .book_sale_inspect import BookSaleInspect


class BookInspectFactory:
    """
    Factory class for creating instances of BookInspector.

    :ivar repo_borrow_line: The repository for borrow lines, used to obtain active borrows for books.
    """
    def __init__(self, repo_borrow_line: BorrowLineRepository):
        self.repo_borrow_line = repo_borrow_line

    def create(self, is_sale: bool) -> BookInspector:
        """
        Create an instance of BookInspector based on the type of inspection needed.

        :param is_sale: A boolean indicating whether the inspection is for a sale (True) or a borrow (False).
        :return: An instance of BookInspector appropriate for the specified type of inspection.
        """
        if is_sale:
            return BookSaleInspect(self.repo_borrow_line)
        else:
            return BookBorrowInspect(self.repo_borrow_line)
