from src.domain.identity.exception import BadRequestError


class UrlRequiredError(BadRequestError):
    def __init__(self, message: str = 'URL is required for summary creation.'):
        super().__init__(message)
