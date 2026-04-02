from src.domain.identity.exception import BadRequestError


class TitleEmptyError(BadRequestError):
    """Exception raised when the title of a book is empty."""

    def __init__(self, message: str = "The title of the book cannot be empty."):
        super().__init__(message)
