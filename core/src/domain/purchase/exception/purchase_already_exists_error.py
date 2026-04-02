from src.domain.identity.exception import BadRequestError


class PurchaseAlreadyExistsError(BadRequestError):
    def __init__(self, message: str = "Purchase already exists"):
        super().__init__(message)
