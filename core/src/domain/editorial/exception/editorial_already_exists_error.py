from src.domain.identity.exception import BadRequestError


class EditorialAlreadyExistsError(BadRequestError):
    def __init__(self, message: str = 'Editorial already exists'):
        super().__init__(message)
