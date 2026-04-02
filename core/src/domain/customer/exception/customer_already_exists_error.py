from src.domain.identity.exception import BadRequestError


class CustomerAlreadyExistsError(BadRequestError):
    def __init__(self, message: str = 'Customer already exists'):
        super().__init__(message)
