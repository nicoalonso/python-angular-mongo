from src.domain.identity.exception import BadRequestError


class InvalidIsbnError(BadRequestError):
    def __init__(self, message: str = 'The ISBN is invalid'):
        super().__init__(message)
