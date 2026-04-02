from src.domain.identity.exception import BadRequestError


class InvalidDeathDateError(BadRequestError):
    def __init__(self, message="Death date cannot be in the future."):
        super().__init__(message)
