from src.domain.identity.exception import BadRequestError


class InvalidBirthDateError(BadRequestError):
    def __init__(self, message="Birth date cannot be in the future."):
        super().__init__(message)
