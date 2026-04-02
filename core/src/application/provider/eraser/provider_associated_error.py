from src.domain.identity.exception import BadRequestError


class ProviderAssociatedError(BadRequestError):
    def __init__(self, message: str = "Provider has purchases and cannot be deleted"):
        super().__init__(message)
