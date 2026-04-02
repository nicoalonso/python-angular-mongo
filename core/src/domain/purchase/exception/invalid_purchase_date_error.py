from src.domain.identity.exception import BadRequestError


class InvalidPurchaseDateError(BadRequestError):
    def __init__(self, message: str = 'The purchase invoice number is required.'):
        super().__init__(message)
