from src.domain.identity.exception import BadRequestError


class InvalidPublishedDateError(BadRequestError):
    def __init__(self, message: str = "Published date cannot be in the future."):
        super().__init__(message)
