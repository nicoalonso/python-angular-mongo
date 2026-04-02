from src.domain.identity.exception import BadRequestError


class AuthorAlreadyExistsError(BadRequestError):
    def __init__(self, message: str = 'Author already exists'):
        super().__init__(message)
