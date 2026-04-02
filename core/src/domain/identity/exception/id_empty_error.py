from .bad_request_error import BadRequestError


class IdEmptyError(BadRequestError):
    def __init__(self, message="ID cannot be empty."):
        super().__init__(message)
