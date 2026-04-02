from src.domain.identity.exception import BadRequestError


class BorrowLinesEmptyError(BadRequestError):
    def __init__(self, message: str = "The borrow must have at least one line."):
        super().__init__(message)
