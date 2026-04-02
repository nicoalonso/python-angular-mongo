from src.domain.identity.exception import BadRequestError


class ProviderAlreadyExistsError(BadRequestError):
    def __init__(self, message: str = 'Provider already exists'):
        super().__init__(message)
