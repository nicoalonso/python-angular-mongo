from src.domain.identity.exception import NotFoundError


class BookNotFoundError(NotFoundError):
    """
    Exception raised when trying to access a book that does not exist in the system.
    """
    def __init__(self, book_id: str):
        self.book_id = book_id
        super().__init__(f"Book with ID {book_id} not found.")
