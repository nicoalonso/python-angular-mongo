from src.domain.identity.exception import BadRequestError


class InvalidBorrowNumberError(BadRequestError):
    def __init__(self, message: str = 'The borrow number is required.'):
        super().__init__(message)
