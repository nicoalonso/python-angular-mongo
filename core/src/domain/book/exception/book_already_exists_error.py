from src.domain.identity.exception import BadRequestError


class BookAlreadyExistsError(BadRequestError):
    """
    Exception raised when trying to create a book that already exists in the system.
    """
    def __init__(self, message: str = 'Book already exists'):
        super().__init__(message)
