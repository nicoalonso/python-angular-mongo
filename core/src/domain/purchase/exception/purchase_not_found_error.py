from src.domain.identity.exception import NotFoundError


class PurchaseNotFoundError(NotFoundError):
    def __init__(self, message: str = 'The purchase was not found.'):
        super().__init__(message)
