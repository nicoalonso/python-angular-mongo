from src.domain.identity.exception import BadRequestError


class BookAssociatedError(BadRequestError):
    def __init__(self, message: str = 'The book is associated with one or more purchases or sales.'):
        super().__init__(message)
