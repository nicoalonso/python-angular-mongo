from src.domain.identity.exception import BadRequestError


class InvalidSaleDateError(BadRequestError):
    def __init__(self, message: str = 'Sale date cannot be in the future.'):
        super().__init__(message)
